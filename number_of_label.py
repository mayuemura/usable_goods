#number_of_label.py
#-*- coding:utf-8 -*-

from collections import defaultdict
from pymongo import Connection


def main():

    client = Connection("beer")
    db = client["usable_goods"]

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

    d_kr = defaultdict(int)
    d_st = defaultdict(int)

    for collection in collections:
        coll = db[collection]

        for label in labels:

            d_kr[label] += int(coll.find({"annotator":"kr", "kr_tag":label}).count())
            d_st[label] += int(coll.find({"annotator":"st", "st_tag":label}).count())

    return d_kr, d_st

if __name__ == "__main__":
    kr, st = main()
    print kr
    print st
