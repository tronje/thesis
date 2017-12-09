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

    for entry in cursor.fetchall():
        if "Canvas" in entry[2]:
            print(f"OMG FINGERPRINTER! {entry[1]}")

    conn.close()


if __name__ == "__main__":
    analyze(DefaultMetric(), "/home/tronje/thesis/data/crawl-data.sqlite")
