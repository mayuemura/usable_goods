#relation_agree.py
#-*- coding:utf-8 -*-
#2015/12/10

import glob
import sys

from pymongo import Connection, ASCENDING
from itertools import izip

client = Connection("gin")
db = client["usable_goods"]


def agreement(relation_list_1, relation_list_2, target_dir):

    client = Connection("gin")
    db = client["usable_goods"]

    coll_seg = db[target_dir]
    coll_rel = db[target_dir+"_rel"]

    for relation1 in relation_list_1:
        result = ""
        articleNo = relation1["articleNo"]

        R1_Arg1segNo = relation1["Arg1"]
        R1_Arg2segNo = relation1["Arg2"]
        R1_RelTag = relation1["tag"]
        R1_Ann = relation1["annotator"]
        
        R1_Arg1Tag = coll_seg.find_one({"articleNo":articleNo, R1_Ann+"_segmentNo":R1_Arg1segNo, "annotator":R1_Ann})
        R1_Arg2Tag = coll_seg.find_one({"articleNo":articleNo, R1_Ann+"_segmentNo":R1_Arg2segNo, "annotator":R1_Ann})
 

        for relation2 in relation_list_2:

            R2_Arg1segNo = relation2["Arg1"]
            R2_Arg2segNo = relation2["Arg2"]
            R2_RelTag = relation2["tag"]
            R2_Ann = relation1["annotator"]

            R2_Arg1Tag = coll_seg.find_one({"articleNo":articleNo, R2_Ann+"_segmentNo":R2_Arg1segNo, "annotator":R2_Ann})
            R2_Arg2Tag = coll_seg.find_one({"articleNo":articleNo, R2_Ann+"_segmentNo":R2_Arg2segNo, "annotator":R2_Ann})
 


            query_arg1 = {"articleNo":articleNo, R1_Ann+"_segmentNo":R1_Arg1segNo, R2_Ann+"_segmentNo":R2_Arg1segNo}
            query_arg2 = {"articleNo":articleNo, R1_Ann+"_segmentNo":R1_Arg2segNo, R2_Ann+"_segmentNo":R2_Arg2segNo}

            if coll_seg.find(query_arg1).count() > 0 and coll_seg.find(query_arg2).count() > 0:
                if R1_RelTag == R2_RelTag:
                    #完全一致
                    if R1_Arg1Tag == R2_Arg1Tag and R1_Arg2Tag == R2_Arg2Tag:
                        result = "Complete"
                    #タグのみ一致
                    elif R1_Arg1Tag == R2_Arg2Tag and R1_Arg2Tag == R2_Arg1Tag:
                        result = "RelationTag"
                    #その他
                    else:
                        result = "Others"

                else:
                    #方向のみ一致
                    if R1_Arg1Tag == R2_Arg1Tag and R1_Arg2Tag == R2_Arg2Tag:
                        result = "Direction"
                    #セグメントの位置のみ一致（タグも方向も違う）
                    elif R1_Arg1Tag == R2_Arg2Tag and R1_Arg2Tag == R2_Arg1Tag:
                        result = "Focus"
                    #その他
                    else:
                        result = "Others"
 
                coll_rel.update({"articleNo":articleNo, "R1_segNo": (R1_Arg1segNo, R1_Arg2segNo), "R2_segNo": (R2_Arg1segNo, R2_Arg2segNo)},{"$set":{
                    "articleNo": articleNo,
                    "R1_segNo": (R1_Arg1segNo, R1_Arg2segNo),
                    "R2_segNo": (R2_Arg1segNo, R2_Arg2segNo),
                    "R1_RelationTag": R1_RelTag,
                    "R2_RelationTag": R2_RelTag,
                    "agree": result}}, upsert=True)
            else:
                coll_rel.update({"articleNo":articleNo, "R1_segNo": (R1_Arg1segNo, R1_Arg2segNo), "R2_segNo": (R2_Arg1segNo, R2_Arg2segNo)},{"$set":{
                    "articleNo": articleNo,
                    "R1_segNo": (R1_Arg1segNo, R1_Arg2segNo),
                    "R2_segNo": (R2_Arg1segNo, R2_Arg2segNo),
                    "R1_RelationTag": R1_RelTag,
                    "R2_RelationTag": R2_RelTag,
                    "agree": "Others"}}, upsert=True)

    coll_rel.create_index([("articleNo", ASCENDING)])
    coll_rel.create_index([("R1_segNo", ASCENDING)])
    coll_rel.create_index([("R2_segNo", ASCENDING)])
    coll_rel.create_index([("R1_RelationTag", ASCENDING)])
    coll_rel.create_index([("R2_RelationTag", ASCENDING)])
    coll_rel.create_index([("agree", ASCENDING)])


def main(target_dir):

    UO = glob.glob(target_dir+"/UO/*.ann")
    ST = glob.glob(target_dir+"/stewart/*.ann")

    UO.sort()
    ST.sort()

    for uo, st in izip(UO, ST):
        No_uo = uo.lstrip(target_dir+"/UO/").split("_")[0]
        No_st = st.lstrip(target_dir+"/stewart/").split("_")[0]

        if not No_uo == No_st:
            print No_uo, No_st, "These files are not about same articles."
            break

        with open(uo, "r") as f1:
            relation_list_1 = list()
            for line in f1:
                l = line.split()
                if line.startswith("T"):
                    continue
                else:
                    Arg1No = l[2].lstrip("Arg1:")
                    Arg2No = l[3].lstrip("Arg2:")
                    rel_info = {
                        "articleNo": No_uo,
                        "relationNo": l[0],
                        "tag": l[1],
                        "Arg1": Arg1No,
                        "Arg2": Arg2No,
                        "annotator": "uo"
                        }
                    relation_list_1.append(rel_info)


        with open(st, "r") as f2:
            relation_list_2 = list()
            for line in f2:
                l = line.split()
                if line.startswith("T"):
                    continue
                else:
                    Arg1No = l[2].lstrip("Arg1:")
                    Arg2No = l[3].lstrip("Arg2:")
                    rel_info = {
                        "articleNo": No_uo,
                        "relationNo": l[0],
                        "tag": l[1],
                        "Arg1": Arg1No,
                        "Arg2": Arg2No,
                        "annotator": "st"
                        }
                    relation_list_2.append(rel_info)

        agreement(relation_list_1, relation_list_2, target_dir)

if __name__ == "__main__":
    main("cosme")
    #main("health")
