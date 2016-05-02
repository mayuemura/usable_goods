#len_of_segment.py
#-*- cording:utf-8 -*-
#2015/12/20
#2016/02/29 modified

import sys

from collections import defaultdict
from pymongo import Connection

def len_of_segment():

    client = Connection("beer")
    db = client["usable_goods_SD"]
    coll_c = db["cosme"]
    coll_h = db["health"]
    coll_n = db["health"]

    dp_d = defaultdict(list)
    st_d = defaultdict(list)

    for document in coll_c.find({"annotator":"dp"}):
        dp_d[document["dp_tag"]].append(len(document["words"].split(" ")))

    for document in coll_h.find({"annotator": "dp"}):
        dp_d[document["dp_tag"]].append(len(document["words"].split(" ")))

    for document in coll_n.find({"annotator": "dp"}):
        dp_d[document["dp_tag"]].append(len(document["words"].split(" ")))

    """
    for document in coll_c.find({"annotator": "st"}):
        st_d[document["st_tag"]].append(len(document["words"].split(" ")))

    for document in coll_h.find({"annotator": "st"}):
        st_d[document["st_tag"]].append(len(document["words"].split(" ")))

    for document in coll_n.find({"annotator": "st"}):
        uo_d[document["dp_tag"]].append(len(document["words"].split(" ")))
    """




    for k, v in dp_d.iteritems():
        yield k, sum(v)*1.0/len(v)

    #yield "--------------"

    #for k, v in st_d.iteritems():
    #    yield k, sum(v)*1.0/len(v)

if __name__ == "__main__":
    for result in len_of_segment():
        print result

#python len_of_segment.py
