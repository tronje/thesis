def record_attributes(cursor, sites, num_visits):
    """Record all relevant attributes fetched by each site."""

    cursor.execute("""
            SELECT site_visits.visit_id, javascript.symbol, site_visits.site_url
            FROM site_visits
                JOIN javascript
                  ON site_visits.visit_id = javascript.visit_id;
            """)

    for entry in cursor.fetchall():
        site_id = entry[0]
        symbol = entry[1]

        if site_id > num_visits:
            break

        if 'userAgent' in symbol:
            sites[site_id].score.user_agent = True

        if 'language' in symbol:
            sites[site_id].score.language = True

        if 'cookieEnabled' in symbol:
            sites[site_id].score.cookie_enabled = True

        if 'localStorage' in symbol:
            sites[site_id].score.local_storage = True

        if 'sessionStorage' in symbol:
            sites[site_id].score.session_storage = True

        if 'colorDepth' in symbol:
            sites[site_id].score.color_depth = True

        if 'platform' in symbol:
            sites[site_id].score.platform = True

        if 'doNotTrack' in symbol:
            sites[site_id].score.do_not_track = True

        if 'oscpu' in symbol:
            sites[site_id].score.cpu = True

        if 'toDataURL' in symbol:
            sites[site_id].score.to_data_url = True

        if 'getImageData' in symbol:
            sites[site_id].score.get_image_data = True

        if 'createDataChannel' in symbol:
            sites[site_id].score.create_data_channel = True

        if 'createOffer' in symbol:
            sites[site_id].score.create_offer = True

        if 'onicecandidate' in symbol:
            sites[site_id].score.onicecandidate = True

        if 'toDataURL' in symbol:
            sites[site_id].score.to_data_url += 1

        if 'measureText' in symbol:
            sites[site_id].score.measure_count += 1


def canvas_sizes(cursor, sites, num_visits):
    cursor.execute(f"""
            SELECT site_visits.visit_id, MAX(javascript.value)
            FROM site_visits
                JOIN javascript
                  ON site_visits.visit_id = javascript.visit_id
            WHERE javascript.symbol = 'HTMLCanvasElement.width'
                AND javascript.operation = 'set'
            GROUP BY site_visits.site_url;
            """)

    for entry in cursor.fetchall():
        # since not every site is guaranteed to have return a row,
        # we might fetch more sites than we're actually looking at.
        # if that happens, just break
        if entry[0] > num_visits:
            break

        sites[entry[0]].score.max_canvas_width = int(float(entry[1]))

    cursor.execute(f"""
            SELECT site_visits.visit_id, MAX(javascript.value)
            FROM site_visits
                JOIN javascript
                  ON site_visits.visit_id = javascript.visit_id
            WHERE javascript.symbol = 'HTMLCanvasElement.height'
                AND javascript.operation = 'set'
            GROUP BY site_visits.site_url;
            """)

    for entry in cursor.fetchall():
        # since not every site is guaranteed to have return a row,
        # we might fetch more sites than we're actually looking at.
        # if that happens, just break
        if entry[0] > num_visits:
            break

        sites[entry[0]].score.max_canvas_height = int(float(entry[1]))
