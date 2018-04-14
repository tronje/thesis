def analyse(site, db_conn):
    cursor = db_conn.cursor()

    query = f"""
        SELECT COUNT(javascript.id)
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND (javascript.symbol LIKE '%audio%'
                 OR javascript.symbol LIKE 'AnalyserNode%'
                 OR javascript.symbol LIKE 'GainNode%'
                 OR javascript.symbol LIKE 'OscillatorNode%'
                 OR javascript.symbol LIKE 'ScriptProcessorNode%');
    """

    cursor.execute(query)

    count = cursor.fetchone()[0]

    return count > 0
