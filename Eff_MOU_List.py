#Eff_MOU_List.py
#-*-coding:utf-8-*-
#2016/02/08

import sys
from pymongo import Connection

def main():

    client = Connection("beer")
    db = client["usable_goods"]
    collections = ["cosme", "health", "nlp2016"]

    with open("Effect.txt", "w") as fe, open("MOU.txt", "w") as fm:
        for collection in collections:
            coll = db[collection]

            for instance in coll.find({"st_tag":"Effect", "annotator":"st"}):
                fe.write(instance["words"]+"\n")

            for instance in coll.find({"st_tag":"MeansOfUse", "annotator":"st"}):
                fm.write(instance["words"]+"\n")

if __name__ == "__main__":
    main()
