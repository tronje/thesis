# TODO review scripts to be sure
fp_scripts = [
    "https://atanx.alicdn.com/t/tanxssp.js%",
    "https://tags.bkrtx.com/js/bk-coretag.js",
    "https://cdn.krxd.net/ctjs/controltag.js%",
    "https://pixel.cdnwidget.com/cdn/c.min.js",
    "https://js.hs-analytics.net/analytics/1517064600000/2249672.js",
    "https://gateway.foresee.com/code/%/fs.utils.js",
    "http://tags.tiqcdn.com/%/utag%",
    "https://d9.flashtalking.com/d9core",
    "https://d1af033869koo7.cloudfront.net/psp/platform/default/247fwk.js",
    "https://vht.tradedoubler.com/fp/prefs.js",
    "https://www.cdn-net.com/cc.js",
    "https://client.perimeterx.net/%/main.min.js",
    "https://api.b2c.com/%",
    "https://js.navigator.io/1",
    "https://c.webtrends.com/acs/common/js/%/common.js",
    "https://static.adsafeprotected.com/sca.%.js",
]


def analyse(site, db_conn):
    cursor = db_conn.cursor()

    script_queries = "script_url LIKE "

    for script in fp_scripts:
        script_queries += "'" + script + "'"
        script_queries += "\n"
        script_queries += "OR script_url LIKE "

    query = f"""
        SELECT DISTINCT script_url
        FROM javascript
            JOIN site_visits
                ON javascript.visit_id = site_visits.visit_id
        WHERE site_visits.site_url LIKE '{site}'
            AND (javascript.script_url LIKE '{fp_scripts[0]}'

    """

    for script in fp_scripts[1:]:
        query += f"OR javascript.script_url LIKE '{script}'\n"

    query += ");"

    cursor.execute(query)

    used_scripts = []

    for row in cursor.fetchall():
        used_scripts.append(row[0])

    return used_scripts
