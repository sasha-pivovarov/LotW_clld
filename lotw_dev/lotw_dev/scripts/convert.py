#encoding: utf8

import sqlite3
import openpyxl

def get_level(strname):
    level = 0
    for char in strname:
        if char == ".":
            level += 1
        else:
            return level

    return level

def get_col_set(table, colname, header_row=1):
    res = []
    column = table[colname]
    for x in range(header_row, len(column)):
        res.append(column[x].value)
    return list(set(res))


wb = openpyxl.load_workbook("excelbase.xlsx")
conn = sqlite3.connect("lotw_base.sqlite")
base = conn.cursor()

feature_table = wb["Feature_value_table"]
language_table = wb["Genealogic_index"]

features = []
languages = []
binary = []
branches = get_col_set(language_table, "E")
families = get_col_set(language_table, "D")
genealogicals = []

count = 0




for line in language_table.rows:
    if count != 0:
        lang_data = {"Id": count, "English_name": line[0].value.strip(), "Number_of_features": None, "Code_ISO_639-3":line[1].value}
        if lang_data["English_name"] in [x["English_name"] for x in languages]:
            continue
        languages.append(lang_data)
        gen_data = {"Id": count, "Lang_id": count, "Fam_id": families.index(line[3].value) + 1,
                    "Branch_id": branches.index(line[4].value) + 1,
                    "Group_id": None, "Subgroup_id": None, "Extinct": line[5].value and ("extinct" in line[5].value.split()),
                    "Koine_language": line[5].value and ("koine" in line[5].value.split())}
        genealogicals.append(gen_data)
        count += 1
    else:
        count += 1

count = 0
bin_count = 1
header = None

processed = set()
for line in feature_table.rows:
    if count > 0:
        feature_data = {"Id": count, "Nomerinv": line[0].value, "Strmod": line[3].value.strip(), "Razdel": line[2].value, "Link_to_wiki": None, "Parent_Id": None}
        level = get_level(line[3].value.strip())
        print("Adding feature %s" % line[3].value)
        for feature in features[::-1]:
            feat_level = get_level(feature["Strmod"])
            if feat_level == (level - 1):
                feature_data["Parent_Id"] = feature["Id"]
                print("Found feature parent")
                break

        features.append(feature_data)
        for i in range(len(header)):
            col_title = header[i]

            data = {"Id": bin_count, "Lang_id":None, "Feat_id": count, "Feature_value": line[i].value, "Reference": None}
            try:
                langs = [x["Id"] for x in languages if x["English_name"] == col_title.value]
                lang = langs[0]
                assert len(langs) == 1
                bin_count += 1
                if not (lang, data["Feat_id"]) in processed:
                    processed.add((lang, data["Feat_id"]))
                else:
                    continue
            except IndexError:
                continue
            data["Lang_id"] = lang

            binary.append(data)
        count += 1
    else:
        header = line
        count += 1

for language in languages:
    language["Number_of_features"] = sum([(x["Lang_id"] == language["Id"] and str(x["Feature_value"]) == "1") for x in binary])




for branch in branches:
    base.execute("INSERT INTO Branch VALUES (?, ?)", (branches.index(branch) + 1, branch))

for family in families:
    base.execute("INSERT INTO Family VALUES (?, ?)", (families.index(family) + 1, family))

for datum in genealogicals:
    base.execute("INSERT INTO Genealogical_index VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (datum["Id"], datum["Lang_id"], datum["Fam_id"], datum["Branch_id"], datum["Group_id"],datum["Subgroup_id"], datum["Extinct"], datum["Koine_language"]))

for feature in features:
    base.execute("INSERT INTO Feature VALUES (?, ?, ?, ?, ?, ?)", (feature["Id"], feature["Nomerinv"], feature["Strmod"], feature["Razdel"], feature["Link_to_wiki"], feature["Parent_Id"]) )

for language in languages:
    base.execute("INSERT INTO Language VALUES (?, ?, ?, ?)", (language["Id"], language["English_name"], language["Number_of_features"], language["Code_ISO_639-3"]))

for feature in binary:
    base.execute("INSERT INTO Binary_data VALUES (?, ?, ?, ?, ?)", (feature["Id"], feature["Lang_id"], feature["Feat_id"], feature["Feature_value"], feature["Reference"]))

conn.commit()
base.close()
conn.close()



    

