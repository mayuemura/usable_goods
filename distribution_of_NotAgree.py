#distribution_of_NotAgree.py
#-*- coding: utf-8 -*-
#2016/03/05

import sys
from collections import defaultdict
from pymongo import Connection

def main():

    client = Connection("beer")
    db = client["usable_goods_SD"]

    collections = ["cosme", "health", "nlp2016"]


    combination = defaultdict(int)

    for collection in collections:
        coll = db[collection]

        for document in coll.find({"agree":"Almost"}):
            dp = document["dp_tag"]
            st = document["st_tag"]
            if combination.get((st, dp)):
                combination[(st, dp)] += 1
            else:
                combination[(dp, st)] += 1

    return combination

if __name__ == "__main__":

    total = sum(main().values())
    for k, v in main().iteritems():
        print "comb:{}\tpair:{}\t{}%".format(k, v, round(v*1.0/total*100, 1))
    print total

#python distribution_of_NotAgree.py
