#make_gazetteer.py
#-*- coding:utf-8 -*-
#2016/02/09

import sys
from pymongo import Connection

def main(label):

    client = Connection("beer")
    db = client["usable_goods"]
    collections = ["cosme", "health", "nlp2016"]

    gazetteer = set()
    for collection in collections:
        coll = db[collection]

        for instance in coll.find({"annotator":"st", "st_tag":label}):
            gazetteer.add(instance["words"]+"\n")

    with open("gztr/"+label+"_gztr.txt", "w") as f:
        f.writelines(gazetteer)


if __name__ == "__main__":
    main(sys.argv[1])

#python make_gazetteer.py Target
