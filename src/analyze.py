#!/usr/bin/env python

import datetime
import sqlite3
# import sys

import record

# from score import Score
from website import Site


def analyze(dbpath, num_sites=None):
    # db connection
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    # grab the number of visits, which is the maximal visit_id
    num_visits = cursor.execute("SELECT MAX(visit_id) FROM site_visits;")
    num_visits = num_visits.fetchone()[0]

    # adjust to however many sites we actually want to analyze
    if num_sites is not None:
        num_visits = num_sites

    # init enormous site dict which we will populate with the info
    # from the db
    sites = {}

    cursor.execute(f"""
            SELECT visit_id, site_url
            FROM site_visits
            LIMIT {num_visits};
            """)

    for entry in cursor.fetchall():
        sites[entry[0]] = Site(entry[1])

    record.record_attributes(cursor, sites, num_visits)
    record.canvas_sizes(cursor, sites, num_visits)

    conn.close()

    # write_results(sites)

    # this is now computed automagically
    # for site_id in sites.keys():
    #     if sites[site_id].score.font_count >= 50 \
    #             and sites[site_id].score.measure_count >= 50:
    #         sites[site_id].score.fp_font = True
    #
    #     if sites[site_id].score.to_data_url \
    #             or sites[site_id].score.get_image_data:
    #         if sites[site_id].score.max_canvas_width > 16 \
    #                 and sites[site_id].score.max_canvas_height > 16:
    #             sites[site_id].score.fp_canvas = True
    #
    #     if sites[site_id].score.create_data_channel \
    #             and sites[site_id].score.create_offer \
    #             and sites[site_id].score.onicecandidate:
    #         sites[site_id].score.fp_webrtc = True

    print("site_url,score")
    for site_id in sites.keys():
        site = sites[site_id]
        print(f"\"{site.url}\",{site.score.value}")


def write_results(sites):
    timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H%M")
    db_name = 'out-' + timestamp + '.sqlite3'

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = ("CREATE TABLE IF NOT EXISTS results ("
             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
             "url TEXT, "
             "font_count INTEGER, "
             "measure_count INTEGER, "
             "to_data_url INTEGER, "
             "get_image_data INTEGER, "
             "create_data_channel INTEGER, "
             "create_offer INTEGER, "
             "onicecandidate INTEGER);")

    cursor.execute(query)

    query = ("CREATE TABLE IF NOT EXISTS canvases ("
             "id INTEGER PRIMARY KEY AUTOINCREMENT, "
             "width INTEGER, "
             "height INTEGER, "
             "site_id INTEGER, "
             "FOREIGN KEY(site_id) REFERENCES results(id));")

    cursor.execute(query)

    for site_id in sites.keys():
        query = ("INSERT INTO results (url, font_count, measure_count, "
                 "to_data_url, get_image_data, create_data_channel, "
                 "create_offer, onicecandidate) "
                 "VALUES ("
                 f"'{sites[site_id]['url']}', "
                 f"{sites[site_id]['font_count']}, "
                 f"{sites[site_id]['measure_count']}, "
                 f"{int(sites[site_id]['to_data_url'])}, "
                 f"{int(sites[site_id]['get_image_data'])}, "
                 f"{int(sites[site_id]['create_data_channel'])}, "
                 f"{int(sites[site_id]['create_offer'])}, "
                 f"{int(sites[site_id]['onicecandidate'])}"
                 ");")

        cursor.execute(query)

        conn.commit()

        # just write max values right now I guess
        max_width = sites[site_id]['canvas_sizes'][0]
        max_height = sites[site_id]['canvas_sizes'][1]

        query = ("INSERT INTO canvases (width, height, site_id)"
                 "VALUES ("
                 f"{max_width}, "
                 f"{max_height}, "
                 f"{site_id});")

        cursor.execute(query)

        conn.commit()

    conn.close()


if __name__ == "__main__":
    analyze(
        "/home/tronje/thesis/data/crawl-data-18-01-27-1506.sqlite3",
        num_sites=None
    )
