def analyse(site, db_conn):
    cursor = db_conn.cursor()

    uses_webgl = f"""
        SELECT DISTINCT symbol
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND javascript.symbol LIKE 'RTCPeerConnection%';
    """

    cursor.execute(uses_webgl)
    count = 0
    onicecandidate = False

    for row in cursor.fetchall():
        if "onicecandidate" in row[0]:
            onicecandidate = True

        count += 1

    if onicecandidate:
        return {
            "uses WebRTC": True,
            "uses onicecandidate": True,
        }
    else:
        return count > 0
