#!/usr/bin/env python3

import csv
import sys


def main():
    f1 = '/home/tronje/thesis/data/fingerprintjs2_users.csv'
    f2 = 'canvas_fpers_8_or_more_attrs.csv'

    file1_entries = []
    file2_entries = []

    with open(f1, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            file1_entries.append(row['site_url'])

    with open(f2, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            file2_entries.append(row['site_url'])

    with open('fp2js_users_overlap.csv', 'w') as f:
        f.write("site_url\n")

        for site in file1_entries:
            if site in file2_entries:
                f.write(site)
                f.write('\n')

    return 0


if __name__ == "__main__":
    sys.exit(main())
