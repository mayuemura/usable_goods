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
    print dp
    print st

    """
    dp_sum = sum(dp.values())
    st_sum = sum(st.values())

    print "Deepika"
    for k, v in dp.iteritems():
        print "{}\t{}\t{}%".format(k, v, round(v*1.0/dp_sum*100,2))
    print dp_sum

    print "-----------"

    print "Stewart"
    for k, v in st.iteritems():
        print "{}\t{}\t{}%".format(k, v, round(v*1.0/st_sum*100,2))
    print st_sum
    """

#python number_of_label.py
