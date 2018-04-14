#!/usr/bin/env python3

# standard library
import json
import sqlite3
import sys

# local modules
import audio
import basics
import canvas
import font
import names
import scripts
import webgl
import webrtc


def get_db_connection(db_file):
    connection = sqlite3.connect(db_file)

    return connection


def aggregate_results(site, db_conn):
    fp_results = {
        "basics": basics.analyse(site, db_conn),
        "audio": audio.analyse(site, db_conn),
        "canvas": canvas.analyse(site, db_conn),
        "font": font.analyse(site, db_conn),
        "suspicious function names": names.analyse(site, db_conn),
        "scripts": scripts.analyse(site, db_conn),
        "webgl": webgl.analyse(site, db_conn),
        "webrtc": webrtc.analyse(site, db_conn),
    }

    return fp_results


def analyse(site, db_file):
    db_conn = get_db_connection(db_file)
    results = aggregate_results(site, db_conn)

    print(json.dumps(results, indent=4))


def main(site_list_file, db_file):
    db_conn = get_db_connection(db_file)
    sites = []

    with open(site_list_file) as f:
        for line in f:
            sites.append(line.strip())

    results = {}

    for site in sites:
        results[site] = aggregate_results(site, db_conn)

    # with open("out.json", "w") as out:
    #     json.dump(results, out, indent=4)

    print(json.dumps(results, indent=4))

    db_conn.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
