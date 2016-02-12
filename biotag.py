#biotag.py
#-*- coding:utf-8 -*-
#2015/12/17
#2016/02/02

import glob
import itertools
import os.path
import re
import sys

from pymongo import Connection

def biotag(dirname):


    #TODO 参照ファイル変更
    ann_filelist = glob.glob("data/{}/stewart/*.ann".format(dirname))
    txt_filelist = glob.glob("data/{}/txt/*.txt".format(dirname))

    ann_filelist.sort()
    txt_filelist.sort()


    #client = Connection("beer")
    #db = client["usable_goods"]
    #coll = db[dirname]

    j = 0
    for ann_file, txt_file in itertools.izip(ann_filelist, txt_filelist):

        with open(txt_file, "r") as ft:
            txt = unicode(ft.read().replace("\n", " "))
            word_list = list()
            word = ""
            start = 0
            for i, letter in enumerate(txt):

                if letter in (" ", ".", ",",")","(",'"', "'", "—", ":", ";", "*", "/", "|"):
                    word_list.append((word, start, i))
                    word = ""
                    start = i+1
                else:
                    word += letter


        with open(ann_file, "r") as fa:
            articleNo = os.path.basename(ann_file).split("_")[0]
            ann_list = list()

            for line in fa:
                if line.startswith("R"):
                    continue
                else:
                    try:
                        l = line.split()
                        ann_dict = {
                            "segmentNo": l[0],
                            "tag": l[1],
                            "start": int(l[2]),
                            "end": int(l[3]),
                            "words": " ".join(l[4:])
                        }
                    except ValueError:
                        print "file:" + ann_file


                    """
                    #mongoに入ってるsegment間の一致でNot_agreeならann_listに入れない
                    agreement = coll.find_one({
                        "articleNo":articleNo,
                        "st_segmentNo":ann_dict["segmentNo"],
                        "annotator":"st"})["agree"]

                    if agreement == "Not_agree":
                        continue
                    else:
                        ann_list.append(ann_dict)
                    """

                    ann_list.append(ann_dict)
            ann_sorted = sorted(ann_list, key=lambda x: x["start"])

            #print txt_file
            """
            if txt_file == "data/nlp2016/txt/050_Nasal_strip.txt":
                for i in word_list:
                    print i
                for j in ann_sorted:
                    print j
                break
            """

        tag_dict = {
                "Target": "Trg",
                "Effect": "Eff",
                "NullEffect": "Null",
                "DegreeOfEffect": "Deg",
                "CertaintyOfEffect": "Cer",
                "ComposedOf": "Com",
                "Location": "Loc",
                "Time": "Time",
                "User": "User",
                "Version": "Ver",
                "MeansOfUse": "MOU",
                "PartOf": "Part"
                }

        #"""
        FLAG = 0
        for info_tuple in word_list:
            w, start, end = info_tuple

            if ann_sorted:
                tag = ann_sorted[0]["tag"]
                ann_start = ann_sorted[0]["start"]
                ann_end = ann_sorted[0]["end"]

                #segmentが1単語で終わる
                if start == ann_start and end == ann_end: 
                    tag = "B-"+tag_dict[tag]
                    ann_sorted.pop(0)
                    FLAG = 0

                #segmentの始め
                elif FLAG == 0 and start == ann_start:
                    tag = "B-"+tag_dict[tag]
                    FLAG = 1

                #segmentの最後
                #segment最後が1個あとになるなどの揺れがあるため
                elif FLAG == 1 and (end == ann_end or end == ann_end-1):
                    tag = "I-"+tag_dict[tag]
                    ann_sorted.pop(0)
                    FLAG = 0
             
                #segmentの中
                elif FLAG == 1 and end < ann_end:
                    tag = "I-"+tag_dict[tag]

                #それ以外
                else:
                    tag = "O"
                    FLAG = 0

            #ann_sortedの中身がないとき
            #そのファイルのアノテーションを適応し終わったあと
            else:
                tag = "O"


            if w == "":
                continue
            else:
                for w_frg in re.split(r"[#|']", w.lstrip("(").rstrip(",:)").replace(".", "|.")):
                    yield w_frg, tag
        yield ""
        #"""

if __name__ == "__main__":
    #biotag(sys.argv[1])
    #"""
    for result in biotag(sys.argv[1]):
        if result == "":
            print ""
        else:
            print "{}\t{}".format(result[0], result[1])
    #"""
