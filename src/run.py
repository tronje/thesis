#!/usr/bin/env python

from __future__ import absolute_import

from automation import TaskManager
from automation import CommandSequence
from automation.SocketInterface import clientsocket

import sys

# The number of sites that we wish to crawl
NUM_SITES = 1000

# number of browsers (visits) per site
NUM_BROWSERS = 4


def determine_canvas_size(table_name, original_url, **kwargs):
    driver = kwargs['driver']
    browser_params = kwargs['browser_params']
    manager_params = kwargs['manager_params']
    crawl_id = browser_params['crawl_id']
    current_url = driver.current_url

    sock = clientsocket()
    sock.connect(*manager_params['aggregator_address'])

    query = ("CREATE TABLE IF NOT EXISTS %s ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "crawl_id INTEGER, "
            "site_url TEXT, "
            "width INTEGER, "
            "height INTEGER, "
            "is_displayed INTEGER)" % table_name)

    sock.send((query, ()))

    canvases = driver.find_elements_by_tag_name('canvas')

    for canvas in canvases:
        width = canvas.size['width']
        height = canvas.size['height']
        displayed = 1 if canvas.is_displayed() else 0

        query = ("INSERT INTO %s (crawl_id, site_url, width, height, is_displayed) "
                "VALUES (?, ?, ?, ?, ?)" % table_name)

        sock.send((query, (crawl_id, current_url, width, height, displayed)))

    sock.close()


def crawl():
    # sites to crawl
    sites = []
    with open("/home/tronje/thesis/data/top-1m.txt", "r") as sitelist:
        for site in sitelist:
            sites.append(site.strip())
            if len(sites) == NUM_SITES:
                break

    # Loads the manager preference and n copies of the default browser dictionaries
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

    # Update TaskManager configuration (use this for crawl-wide settings)
    manager_params['data_directory'] = '~/data/'
    manager_params['log_directory'] = '~/data/'

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    # Visits the sites with all browsers simultaneously
    for site in sites:
        command_sequence = CommandSequence.CommandSequence(site)

        # Start by visiting the page
        command_sequence.get(sleep=5, timeout=60)

        command_sequence.run_custom_function(determine_canvas_size, ('canvases', site))

        # dump_profile_cookies/dump_flash_cookies closes the current tab.
        command_sequence.dump_profile_cookies(120)

        # index='**' synchronizes visits between the three browsers
        manager.execute_command_sequence(command_sequence, index='**')

    # Shuts down the browsers and waits for the data to finish logging
    manager.close()


if __name__ == "__main__":
    crawl()
