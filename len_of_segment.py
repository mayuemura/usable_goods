#len_of_segment.py
#-*- cording:utf-8 -*-
#2012/12/20

import sys

from collections import defaultdict
from pymongo import Connection

def len_of_segment():

    client = Connection("gin")
    db = client["usable_goods"]
    coll_c = db["cosme"]
    coll_h = db["health"]

    uo_d = defaultdict(list)
    st_d = defaultdict(list)

    for document in coll_c.find({"annotator":"uo"}):
        uo_d[document["uo_tag"]].append(len(document["words"].split(" ")))

    for document in coll_h.find({"annotator": "uo"}):
        uo_d[document["uo_tag"]].append(len(document["words"].split(" ")))

    for document in coll_c.find({"annotator": "st"}):
        st_d[document["st_tag"]].append(len(document["words"].split(" ")))

    for document in coll_h.find({"annotator": "st"}):
        st_d[document["st_tag"]].append(len(document["words"].split(" ")))

    for k, v in uo_d.iteritems():
        yield k, sum(v)*1.0/len(v)

    yield "--------------"

    for k, v in st_d.iteritems():
        yield k, sum(v)*1.0/len(v)

if __name__ == "__main__":
    for result in len_of_segment():
        print result

