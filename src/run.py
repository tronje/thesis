#!/usr/bin/env python

from __future__ import absolute_import

from automation import TaskManager
from automation import CommandSequence
from automation.SocketInterface import clientsocket

import datetime

# The number of sites that we wish to crawl
NUM_SITES = 2000

# number of browsers (visits) per site
NUM_BROWSERS = 4


def determine_canvas_properties(table_name, original_url, **kwargs):
    driver = kwargs['driver']
    browser_params = kwargs['browser_params']
    manager_params = kwargs['manager_params']
    crawl_id = browser_params['crawl_id']

    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    query = ("CREATE TABLE IF NOT EXISTS %s ("
             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
             "crawl_id INTEGER, "
             "site_url TEXT, "
             "width INTEGER, "
             "height INTEGER, "
             "is_displayed INTEGER);" % table_name)

    sock.send((query, ()))

    canvases = driver.find_elements_by_tag_name('canvas')

    query = ("INSERT INTO %s (crawl_id, site_url, width, height, is_displayed) "
             "VALUES (?, ?, ?, ?, ?)" % table_name)

    for canvas in canvases:
        width = canvas.size['width']
        height = canvas.size['height']
        displayed = 1 if canvas.is_displayed() else 0

        sock.send((
                query,
                (int(crawl_id),
                 original_url,
                 int(width),
                 int(height),
                 int(displayed))
                ))

    sock.close()


def crawl(sites):
    current_site = None

    try:
        # Loads the manager preference and n copies of the default browser dictionaries
        manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

        # customize browser parameters
        for i in range(NUM_BROWSERS):
            browser_params[i]['disable_flash'] = True
            browser_params[i]['headless'] = True
            browser_params[i]['bot_mitigation'] = False
            browser_params[i]['http_instrument'] = True
            browser_params[i]['js_instrument'] = True
            browser_params[i]['headless'] = True

        # Update TaskManager configuration (use this for crawl-wide settings)
        manager_params['data_directory'] = '~/data/'
        manager_params['log_directory'] = '~/data/'

        timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H%M")
        db_name = 'crawl-data-' + timestamp + '.sqlite3'

        manager_params['database_name'] = db_name

        # Instantiates the measurement platform
        # Commands time out by default after 60 seconds
        manager = TaskManager.TaskManager(manager_params, browser_params)

        # Visits the sites with all browsers simultaneously
        for site in sites:
            current_site = site

            command_sequence = CommandSequence.CommandSequence(site)

            # Start by visiting the page
            command_sequence.get(sleep=10, timeout=60)

            command_sequence.run_custom_function(determine_canvas_properties, ('canvases', site))

            # dump_profile_cookies/dump_flash_cookies closes the current tab.
            command_sequence.dump_profile_cookies(120)

            # index=None sends the command to the first available browser
            # index='*' sends command to all browsers
            # index='**' synchronizes visits between all browsers
            manager.execute_command_sequence(command_sequence, index=None)

        # Shuts down the browsers and waits for the data to finish logging
        manager.close()
    except Exception as e:
        print(e)
        return current_site


def run(filename):
    # sites to crawl
    sites = []
    with open(filename, "r") as sitelist:
        for site in sitelist:
            sites.append(site.strip())
            if len(sites) == NUM_SITES:
                break

    # if we fail at a certain site, we remove it from the list and try again
    while True:
        failed_site = crawl(sites)

        if failed_site is None:
            break

        failed_idx = sites.index(failed_site)
        sites = sites[(failed_idx + 1):]


if __name__ == "__main__":
    run("/home/tronje/thesis/data/top-1m.txt")
