#!/usr/bin/env python3

import csv
import sys


def main():
    files = []

    files.append('/home/tronje/thesis/data/useragent_users.csv')
    files.append('/home/tronje/thesis/data/language_users.csv')
    files.append('/home/tronje/thesis/data/colordepth_users.csv')
    files.append('/home/tronje/thesis/data/local_storage_users.csv')
    files.append('/home/tronje/thesis/data/platform_users.csv')
    files.append('/home/tronje/thesis/data/session_storage_users.csv')
    files.append('/home/tronje/thesis/data/cookieenabled_users.csv')
    files.append('/home/tronje/thesis/data/donottrack_users.csv')
    files.append('/home/tronje/thesis/data/oscpu_users.csv')

    file_entries = [[] for i in range(9)]

    all_sites = set()

    for f in files:
        with open(f, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                file_entries[files.index(f)].append(row['site_url'])
                all_sites.add(row['site_url'])

    num_attrs = {}
    for site in all_sites:
        num_attrs[site] = 0

        for entry in file_entries:
            if site in entry:
                num_attrs[site] += 1

    least_2 = 0
    least_3 = 0
    least_4 = 0
    least_5 = 0
    least_6 = 0
    least_7 = 0
    least_8 = 0
    least_9 = 0

    for site in num_attrs.keys():
        if num_attrs[site] >= 2:
            least_2 += 1

        if num_attrs[site] >= 3:
            least_3 += 1

        if num_attrs[site] >= 4:
            least_4 += 1

        if num_attrs[site] >= 5:
            least_5 += 1

        if num_attrs[site] >= 6:
            least_6 += 1

        if num_attrs[site] >= 7:
            least_7 += 1

        if num_attrs[site] >= 8:
            least_8 += 1

        if num_attrs[site] >= 9:
            least_9 += 1

    print(f"at least 2: {least_2}, percentage: {least_2 / 4929}")
    print(f"at least 3: {least_3}, percentage: {least_3 / 4929}")
    print(f"at least 4: {least_4}, percentage: {least_4 / 4929}")
    print(f"at least 5: {least_5}, percentage: {least_5 / 4929}")
    print(f"at least 6: {least_6}, percentage: {least_6 / 4929}")
    print(f"at least 7: {least_7}, percentage: {least_7 / 4929}")
    print(f"at least 8: {least_8}, percentage: {least_8 / 4929}")
    print(f"at least 9: {least_9}, percentage: {least_9 / 4929}")


    with open('using_8_or_more_attributes.csv', 'w') as f:
        f.write("site_url\n")

        for site in num_attrs.keys():
            if num_attrs[site] >= 8:
                f.write(site)
                f.write('\n')

    return 0


if __name__ == "__main__":
    sys.exit(main())
