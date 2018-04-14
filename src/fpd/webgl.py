def analyse(site, db_conn):
    cursor = db_conn.cursor()

    uses_webgl = f"""
        SELECT COUNT(javascript.id)
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND javascript.symbol LIKE '%getcontext%'
            AND javascript.arguments LIKE '%webgl%';
    """

    cursor.execute(uses_webgl)

    count = cursor.fetchone()[0]

    return count > 0
