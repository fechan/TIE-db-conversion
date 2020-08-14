#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""json_to_tie_db.py: Adds entries from the JSON of parsed OCR text generated by parse_ocr_txt.py
into the travelers_in_egypt SQLite database
"""

import json
import sqlite3
import re

DATABASE_FILE = "travelers_in_egypt.sqlite3"
JSON_FILE = "ocr_parsed.json"

input_file = open(JSON_FILE)
entries = json.load(input_file)
input_file.close()
connection = sqlite3.connect(DATABASE_FILE)
db = connection.cursor()

for entry in entries:
    db.execute("""INSERT INTO travelers (name, nationality)
                  VALUES (?, ?)""", (entry["name"].rstrip(), entry["nationality"].rstrip()))
    traveler_id = db.lastrowid

    for work in entry["works"]:
        publication = (
            entry["travel_date"].rstrip(),
            re.sub(r"[ab]. ?", "", work["title"]).rstrip(),
            work["publishing_info"].rstrip(),
            re.sub(r"[ab]. ?", "", work["annotation"]).rstrip(),
            traveler_id
        )
        db.execute("""INSERT INTO publications (travel_dates, title, publisher_misc, summary, traveler_id)
                      VALUES (?, ?, ?, ?, ?)""", publication)

connection.commit()