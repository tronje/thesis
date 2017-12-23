#!/usr/bin/env python

import sqlite3
from metric import DefaultMetric


def analyze(metric, dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    num_visits = cursor.execute("SELECT MAX(visit_id) FROM site_visits;")
    num_visits = num_visits.fetchone()[0]
    print(f"{num_visits} site visits")

    cursor.execute("""
            SELECT site_visits.visit_id, site_url, symbol
            FROM site_visits
                JOIN javascript
                  ON site_visits.visit_id = javascript.visit_id;
            """)

    sites = {}
    for i in range(1, num_visits + 1):
        sites[i] = {
                'url': None,
                'font_count': 0,
                'measure_count': 0,
                'to_data_url': False,
                'get_image_data': False,
                'create_data_channel': False,
                'create_offer': False,
                'onicecandidate': False,
                'fp_font': False,
                'fp_canvas': False,
                'fp_webrtc': False,
                }


    for entry in cursor.fetchall():
        _id = entry[0]
        _url = entry[1]
        _symbol = entry[2]

        if sites[_id]['url'] is None:
            sites[_id]['url'] = _url

        if "font" in entry[2]:
            sites[_id]['font_count'] += 1
        if "measureText" in entry[2]:
            sites[_id]['measure_count'] += 1
        if "toDataURL" in entry[2]:
            sites[_id]['to_data_url'] = True
        if "getImageData" in entry[2]:
            sites[_id]['get_image_data'] = True
        if "createDataChannel" in entry[2]:
            sites[_id]['create_data_channel'] = True
        if "createOffer" in entry[2]:
            sites[_id]['create_offer'] = True
        if "onicecandidate" in entry[2]:
            sites[_id]['onicecandidate'] = True

    conn.close()


    for _id in sites.keys():
        if sites[_id]['font_count'] >= 50 and sites[_id]['measure_count'] >= 50:
            sites[_id]['fp_font'] = True

        if sites[_id]['to_data_url'] and sites[_id]['get_image_data']:
            sites[_id]['fp_canvas'] = True

        if sites[_id]['create_data_channel'] and sites[_id]['create_offer'] \
                and sites[_id]['onicecandidate']:
            sites[_id]['fp_webrtc'] = True


    for _id in sites.keys():
        if sites[_id]['fp_font'] or sites[_id]['fp_canvas'] or sites[_id]['fp_webrtc']:
            print(f"""{sites[_id]['url']}
                    font: {sites[_id]['fp_font']}
                    canvas: {sites[_id]['fp_canvas']}
                    webrtc: {sites[_id]['fp_webrtc']}""")
            print()


if __name__ == "__main__":
    analyze(DefaultMetric(), "/home/tronje/thesis/data/crawl-data.sqlite")
