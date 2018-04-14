def analyse(site, db_conn):
    cursor = db_conn.cursor()
    results = {}

    query = f"""
        SELECT COUNT(javascript.id)
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND javascript.symbol LIKE '%font'
            AND javascript.operation LIKE 'set';
    """
    cursor.execute(query)
    count = cursor.fetchone()[0]
    results["fonts set"] = count

    query = f"""
        SELECT COUNT(javascript.id)
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND symbol LIKE 'CanvasRenderingContext2D.measureText';
    """
    cursor.execute(query)
    count = cursor.fetchone()[0]
    results["measureText calls"] = count

    query = f"""
        SELECT COUNT(javascript.id)
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND javascript.arguments LIKE '%mmmmmmmmmmlli%';
    """
    cursor.execute(query)
    count = cursor.fetchone()[0]
    results["uses 'mmmmmmmmmmlli' magic string"] = count > 0

    query = f"""
        SELECT COUNT(javascript.id)
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND javascript.arguments LIKE '%Cwm fjordbank glyphs vext quiz%';
    """
    cursor.execute(query)
    count = cursor.fetchone()[0]
    results["uses 'Cwm fjordbank glyphs vext quiz' magic string"] = count > 0

    return results
