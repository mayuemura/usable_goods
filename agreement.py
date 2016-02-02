#agreement.py
#-*- coding:utf-8 -*-
#2016/01/11
#2016/01/12 Targetなしのagreeのみ表示

from collections import defaultdict
from pymongo import Connection

def main():

    client = Connection("beer")
    db = client["usable_goods"]

    collections = ["cosme", "health", "nlp2016"]

    agreements = ["Complete", "Overlap", "ProperSub", "Surface", "End", "Start", "Almost", "Not_agree"]

    d_ag = defaultdict(int)
    number_of_instance = 0

    for collection in collections:
        coll = db[collection]
        #number_of_instance += int(coll.find().count())
        number_of_instance += int(coll.find({"$or":[{"kr_tag":{"$ne":"Target"}},{"st_tag":{"$ne":"Target"}}]}).count())

        for agreement in agreements:
            d_ag[agreement] += int(coll.find({"agree":agreement, "$or":[{"kr_tag":{"$ne":"Target"}},{"st_tag":{"$ne":"Target"}}]}).count())
            #d_ag[agreement] += int(coll.find({"agree":agreement}).count())

    print d_ag
    for k, v in d_ag.iteritems():
        yield k, v*1.0/number_of_instance*100

if __name__ == "__main__":
    for ag in main():
        print ag
