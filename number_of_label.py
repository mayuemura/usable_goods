#number_of_label.py
#-*- coding:utf-8 -*-

from collections import defaultdict
from pymongo import Connection


def main():

    client = Connection("beer")
    db = client["usable_goods_SD"]

    collections = ["cosme", "health", "nlp2016"]
    labels = [
            "Target",
            "Effect",
            "CertaintyOfEffect",
            "DegreeOfEffect",
            "NullEffect",
            "MeansOfUse",
            "ComposedOf",
            "PartOf",
            "Location",
            "Time",
            "User",
            "Version"
            ]

    d_dp = defaultdict(int)
    d_st = defaultdict(int)

    for collection in collections:
        coll = db[collection]

        for label in labels:

            d_dp[label] += int(coll.find({"annotator":"dp", "dp_tag":label}).count())
            d_st[label] += int(coll.find({"annotator":"st", "st_tag":label}).count())

    return d_dp, d_st

if __name__ == "__main__":
    dp, st = main()
    for k, v in dp.iteritems():
        print "Deepika"
        print "{}\t{}".format(k, v)

    for k, v in st.iteritems():
        print "Stewart"
        print "{}\t{}".format(k, v)


#python number_of_label.py
