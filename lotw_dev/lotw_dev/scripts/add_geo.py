#encoding: utf8
import openpyxl
import sqlite3


def get_col_set(table, colname, header_row=1):
    res = []
    column = table[colname]
    for x in range(header_row, len(column)):
        res.append(column[x].value)
    return list(set(res))

wb = openpyxl.load_workbook("coordinates-final.xlsx")
conn = sqlite3.connect("lotw_base.sqlite")

table = wb[u"Лист1"]
entries = []
countries = get_col_set(table, "C")
cursor = conn.cursor()
count = 0

for line in table.rows:
    if count != 0:
        name = line[1].value
        country_id = countries.index(line[2].value) + 1
        lat = line[3].value
        long = line[4].value
        lang = cursor.execute("SELECT * FROM Language WHERE English_name=?", (name,)).fetchone()
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