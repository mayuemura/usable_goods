#segment_agree.py
#-*- coding:utf-8 -*-
#2015/12/08
#2016/01/11 modified (St, Kr)
#2016/01/20 modified (added Almost)

import glob
import sys

from itertools import izip
from pymongo import Connection, ASCENDING


def agreement(segment_list_1, segment_list_2):

    for segment1 in segment_list_1:
        result = ""
        s_1 = segment1["start"]
        e_1 = segment1["end"]

        for i, segment2 in enumerate(segment_list_2, start=1):
            s_2 = segment2["start"]
            e_2 = segment2["end"]

            if segment1["tag"] == segment2["tag"]:
                #完全一致
                if segment1["words"] == segment2["words"]:
                    result = "Complete"

                #部分的に重なる
                elif (s_1 < s_2 < e_1 and s_2 < e_1 < e_2) or (s_2 < s_1 < e_2 and s_1 < e_2 < e_1):
                    result = "Overlap"

                #片方がもう片方を真に含む
                elif (s_1 < s_2 and e_2 < e_1) or (s_2 < s_1 and e_1 < e_2):
                    result = "ProperSub"


                #範囲の最初のみ一致
                elif s_1 == s_2 and e_1 != e_2:
                    result = "Start"

                #範囲の最後のみ一致
                elif e_1 == e_2 and s_1 != s_2:
                    result = "End"

                #一致しない
                else:
                    result = "Not_agree" #continueのkey


            else:
                #文字のみ一致
                if segment1["words"] == segment2["words"]:
                    result = "Surface"

                #以下、ラベルが違って範囲がずれてる
                #部分的に重なる
                elif (s_1 < s_2 < e_1 and s_2 < e_1 < e_2) or (s_2 < s_1 < e_2 and s_1 < e_2 < e_1):
                    result = "Almost"

                #片方がもう片方を真に含む
                elif (s_1 < s_2 and e_2 < e_1) or (s_2 < s_1 and e_1 < e_2):
                    result = "Almost"


                #範囲の最初のみ一致
                elif s_1 == s_2 and e_1 != e_2:
                    result = "Almost"

                #範囲の最後のみ一致
                elif e_1 == e_2 and s_1 != s_2:
                    result = "Almost"


                #一致しない
                else:
                    result = "Not_agree" #continueのkey

            #最後にNot_agreeだったら
            if result == "Not_agree": #continueのkey
                if i == len(segment_list_2):
                    yield [segment1["words"], segment1["tag"], segment1["segmentNo"], None, None, result]
                else:
                    continue

            #Not_agree以外だったら
            else:
                yield [segment1["words"], segment1["tag"], segment1["segmentNo"], segment2["tag"], segment2["segmentNo"], result]
                break

def main(target_dir):

    client = Connection("beer")
    db = client["usable_goods"]
    coll = db[target_dir]

    #UO = glob.glob("data/"+target_dir+"/UO/*.ann")
    ST = glob.glob("data/"+target_dir+"/stewart/*.ann")
    KR = glob.glob("data/"+target_dir+"/kirin/*.ann")

    #UO.sort()
    ST.sort()
    KR.sort()

    #以降，すべてUO-->KR
    
    for kr, st in izip(KR, ST):
        No_kr = kr.replace("data/"+target_dir+"/kirin/", "").split("_")[0]
        No_st = st.replace("data/"+target_dir+"/stewart/", "").split("_")[0]
        print No_kr, No_st
        if not No_kr == No_st:
            print No_kr, No_st, "These files are not about same articles."
            break
            

        with open(kr, "r") as f1:
            segment_list_1 = list()
            for line in f1:
                l = line.split()
                ann_info = dict()

                if line.startswith("R") or line.startswith("#"):
                    continue
                else:
                    try:
                        words = " ".join(l[4:])
                        end = int(l[3])

                        if words.endswith((".", ",")):
                            words = words.rstrip(".,")
                            end = end-1

                        ann_info = {
                            "segmentNo": l[0],
                            "tag": l[1],
                            "start": int(l[2]),
                            "end": end,
                            "words": words
                            }

                        segment_list_1.append(ann_info)
                    except ValueError:
                        print "file: " + kr


        with open(st, "r") as f2:
            segment_list_2 = list()
            for line in f2:
                l = line.split()
                ann_info = dict()

                if line.startswith("R"):
                    continue
                else:
                    try:
                        words = " ".join(l[4:])
                        end = int(l[3])

                        if words.endswith((".", ",")):
                            words = words.rstrip(".,")
                            end = end-1

                        ann_info = {
                            "segmentNo": l[0],
                            "tag": l[1],
                            "start": int(l[2]),
                            "end": end,
                            "words": words
                            }

                        segment_list_2.append(ann_info)
                    except ValueError:
                        print "file: " + st



        for iteration in agreement(segment_list_1, segment_list_2):
            coll.update({"articleNo":No_kr, "kr_segmentNo":iteration[2], "annotator": "kr"}, {"$set": {
                "annotator": "kr",
                "words": iteration[0],
                "kr_tag": iteration[1],
                "kr_segmentNo": iteration[2],
                "st_tag": iteration[3],
                "st_segmentNo": iteration[4],
                "agree": iteration[5],
                "articleNo": No_kr}}, upsert = True)


        for iteration in agreement(segment_list_2, segment_list_1):
            coll.update({"articleNo":No_kr, "st_segmentNo":iteration[2], "annotator": "st"}, {"$set": {
                "annotator": "st",
                "words": iteration[0],
                "st_tag": iteration[1],
                "st_segmentNo": iteration[2],
                "kr_tag": iteration[3],
                "kr_segmentNo": iteration[4],
                "agree": iteration[5],
                "articleNo": No_kr}}, upsert = True)


    coll.create_index([("annotator", ASCENDING)])
    coll.create_index([("words", ASCENDING)])
    coll.create_index([("kr_tag", ASCENDING)])
    coll.create_index([("st_tag", ASCENDING)])
    coll.create_index([("articleNo", ASCENDING)])
    coll.create_index([("segmentNo", ASCENDING)])
    coll.create_index([("agree", ASCENDING)])


if __name__ == "__main__":
    main(sys.argv[1])
    #main("health")
    #main("nlp2016")
