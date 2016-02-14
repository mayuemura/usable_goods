#label_list.py
#-*-coding:utf-8-*-
#2016/02/08

import sys
from pymongo import Connection

def main(label):

    client = Connection("beer")
    db = client["usable_goods"]
    collections = ["cosme", "health", "nlp2016"]

    with open(label+".txt", "w") as f:
        for collection in collections:
            coll = db[collection]

            for instance in coll.find({"st_tag":label, "annotator":"st"}):
                f.write(instance["words"]+"\n")

if __name__ == "__main__":
    main(sys.argv[1])

#python label_list.py Effect
