#phrase_checker.py
#-*- coding: utf-8 -*-


import sys
from pymongo import Connection

def main(label):

    client = Connection("beer")
    db = client["usable_goods_SD"]
    collections = ["cosme", "health", "nlp2016"]

    with open(label+"_annotated.txt", "r") as f:
        for line in f:
            words = line.rstrip("\n").split("\t")[-1]
            FLAG = 0
            for collection in collections:
                coll = db[collection]
                query = {"words":words, "dp_tag":label}
                if coll.find(query).count() > 0:
                    FLAG = 1
            if FLAG == 0:
                print line

def main_op(label):

    client = Connection("beer")
    db = client["usable_goods_SD"]
    collections = ["cosme", "health", "nlp2016"]

    with open(label+"_annotated.txt", "r") as f:
        words_set = set()
        for collection in collections:
            coll = db[collection]
            for document in coll.find({"dp_tag":label}):
                words_set.add(document["words"])

        for line in f:
            words = line.rstrip("\n").split("\t")[-1]
            if words in words_set:
                continue
            else:
                print line



if __name__ == "__main__":
    main_op(sys.argv[1])

#python phsase_checker.py Effect
