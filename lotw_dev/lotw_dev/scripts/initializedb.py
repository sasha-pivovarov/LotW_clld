#encoding: utf8

from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import lotw_dev
from lotw_dev import models
from lotw_dev.models import ClosureTable, TreeFeature, lotw_devLanguage

import sqlite3

# feat_name_counts = {}
# def convert_feature(feature):
#     global feat_name_counts
#     if feature[2] not in feat_name_counts:
#         return feature
#     else:
#         feature[2] = feature[2] + "_" + feat_name_counts[feature[2]][1]
#         feat_name_counts[feature[2]][1] += 1
#         return feature
#
def main(args):
    data = Data()
    lotw_conn = sqlite3.connect("lotw_base.sqlite")
    lotw_base = lotw_conn.cursor()
    contrib = common.Contribution(id="initial_contrib",
                                  name="Initial contribution")


    dataset = common.Dataset(id=lotw_dev.__name__,
                             domain='lotw_dev.clld.org',
                             name="Languages of the World",
                             publisher_name="IL RAS",
                             publisher_place="Moscow",
                             publisher_url="http://iling-ran.ru/main/",
                             jsondata={
                                 'license_name': 'Creative Commons Attribution 4.0 International License'}
                             )
    DBSession.add(dataset)
    feature_dict = {}
    unnamed_feature_count = 0
    features = lotw_base.execute("SELECT * FROM Feature").fetchall()
    names = [y[2] for y in features]
    feat_name_counts = {x[2]: [names.count(x[2]), 0] for x in features if names.count(x[2]) > 1}

    # features = [convert_feature(x) for x in features]

    for feature in features:
        name = feature[2]
        # if name == ".О":
        #     continue
        if name in feat_name_counts.keys():
            temp_name = name
            name += ("_" + str(feat_name_counts[name][1]))
            feat_name_counts[temp_name][1] += 1

        feature_dict[feature[0]] = TreeFeature(pk=feature[0],
                                               id=feature[0],
                                             name=name,
                                               father_pk=feature[5])
        print("Added feature %s" % feature[2])

    langs = lotw_base.execute("SELECT * FROM Language").fetchall()
    assert len(set([lang[0] for lang in langs])) == len([lang[0] for lang in langs])
    for language in langs:
        value_sets = []
        geodata = lotw_base.execute("SELECT * FROM Geographical_index WHERE Lang_id=?", (str(language[0]), )).fetchone()
        famdata = lotw_base.execute("SELECT * FROM Genealogical_index WHERE Lang_id=?", (str(language[0]), )).fetchone()
        famname = lotw_base.execute("SELECT * FROM Family where Id=?", (famdata[2], )).fetchone()[1]
        branchname =lotw_base.execute("SELECT * FROM Branch where Id=?", (famdata[3], )).fetchone()[1]
        if not geodata:
            geodata = [0.0 for x in range(7)]
        data.add(lotw_devLanguage, language[0],
                 id=str(language[0]),
                 iso=language[3],
                 family=famname,
                 branch=branchname,
                 name=language[1],
                 latitude=geodata[5],
                 longitude=geodata[6])

        print("Added language %s" % language[3])
        # Lang_id=language["Lang_id"], Order_of_addition=language["Order_of_addition"],
                # Sorting_number=language["Sorting_number"], Code_ISO_639_3=language["Code_ISO_639_3"]
        language_features = lotw_base.execute("SELECT * FROM Binary_data WHERE Lang_id=? AND Feature_value=1", (str(language[0]), ))
        for l_feat in language_features.fetchall():
            feat_id = l_feat[0]
            try:
                feat_name = feature_dict[l_feat[2]].name
            except KeyError:
                continue

            vs = common.ValueSet(id=feat_id,
                                 language=data["lotw_devLanguage"][language[0]],
                                 parameter=feature_dict[l_feat[2]],
                                 contribution=contrib)
            DBSession.add(common.Value(id=feat_id,
                                       name=feat_name,
                                       valueset=vs))
            print("Added value %s" % feat_id)





    lotw_conn.close()




def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    DBSession.execute('delete from closuretable')
    SQL = ClosureTable.__table__.insert()

    # store a mapping of pk to father_pk for all languoids:
    father_map = {r[0]: r[1] for r in DBSession.execute('select pk, father_pk from treefeature')}

    # we compute the ancestry for each single languoid
    for pk, father_pk in father_map.items():
        depth = 1

        # now follow up the line of ancestors
        while father_pk:
            DBSession.execute(SQL, dict(child_pk=pk, parent_pk=father_pk, depth=depth))
            depth += 1
            father_pk = father_map[father_pk]


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
