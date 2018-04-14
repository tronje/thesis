# suspicious function names
# all lower case because SQLite's `LIKE` is not case sensitive
suspicious_names = [
    '%fingerprint%',
    '%fingerprint%',
    '%getfingerprint%',
    '%getfp%',
    '%getcanvasfp%',
    '%getcanvasprint%',
    '%getcanvasfingerprint%',
    '%getaudioprint%',
    '%getaudiofingerprint%',
    '%gethaslied%',
]


def analyse(site, db_conn):
    cursor = db_conn.cursor()

    query = """
        SELECT func_name
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND javascript.func_name LIKE '{name}';
    """

    found_names = set()

    for name in suspicious_names:
        cursor.execute(query.format(site=site, name=name))

        for row in cursor.fetchall():
            found_names.add(row[0])

    return list(found_names)
