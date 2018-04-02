#encoding: utf8
import openpyxl
import sqlite3
from string import punctuation
import re
from Levenshtein import distance


def get_col_set(table, colname, header_row=1):
    res = []
    column = table[colname]
    for x in range(header_row, len(column)):
        res.append(column[x].value)
    return list(set(res))

rexp = re.compile("[%s]"%punctuation)

def is_close(str1, str2):
    str1l = rexp.sub("", str1.lower())
    str2l = rexp.sub("", str2.lower())
    if distance(str1l, str2l) < 2:
        return True

    return False

wb = openpyxl.load_workbook("coordinates-final.xlsx")
conn = sqlite3.connect("lotw_base.sqlite")

table = wb[u"Лист1"]
entries = []
countries = get_col_set(table, "C")
cursor = conn.cursor()
count = 0
langs_in_base = cursor.execute("SELECT * FROM Language").fetchall()
for line in table.rows:
    if count != 0:
        name = line[1].value
        country_id = countries.index(line[2].value) + 1
        lat = line[3].value
        long = line[4].value
        try:
            lang = [x for x in langs_in_base if is_close(x[1], name)][0]
        except IndexError:
            continue
        if lang:
            lang_id = lang[0]
            fam_id = cursor.execute("SELECT * FROM Genealogical_index where Lang_id=?", (lang_id,)).fetchone()[2]
        else:
            continue

        entries.append((count, lang_id, fam_id, country_id, None, lat, long))
        print("line %s processed" % count)
        count += 1
    else:
        count += 1

for id, country in enumerate(countries, start=1):
    cursor.execute("INSERT INTO Country VALUES(?, ?)", (id, country))
for entry in entries:
    cursor.execute("INSERT INTO Geographical_index VALUES (?, ?, ?, ?, ?, ?, ?)", entry)

conn.commit()
conn.close()