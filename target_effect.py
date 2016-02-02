#target_effect.py
#-*- coding: utf-8 -*-
#2016/01/20

import glob
import itertools
import os.path
import sys

def tag_collection(annotator):

    trg_eff = list()
    other = list()

    collections = ["cosme", "health", "nlp2016"]

    for coll in collections:
        txt_filelist = sorted(glob.glob("data/{}/txt/*.txt".format(coll)))
        ann_filelist = sorted(glob.glob("data/{}/{}/*.ann".format(coll, annotator)))


        for ann_file, txt_file in itertools.izip(ann_filelist, txt_filelist):
        #for ann_file, txt_file in itertools.izip(["data/nlp2016/kirin/021_Fish_oil.ann"],["data/nlp2016/txt/021_Fish_oil.txt"]):
            ann_article = os.path.basename(ann_file).split(".")[0]
            txt_article = os.path.basename(txt_file).split(".")[0]

            #print (ann_article, txt_article)

            assert ann_article == txt_article, "article No error"

            with open(txt_file, "r") as ft:
                oneline_list = list()
                txt = ft.read()
                oneline = ""
                start = 0
                num = 1
                for i, letter in enumerate(txt):
                    if letter == "\n":
                        if not oneline == "":   #空行除去
                            oneline_list.append({
                                "oneline": oneline,
                                "start": start,
                                "end": i-1,
                                "line_num": num})
                            oneline = ""
                            start = i+1
                            num += 1
                    else:
                        oneline += letter

            #if txt_file == "data/nlp2016/txt/021_Fish_oil.txt":
            #for item in oneline_list:
            #    print item

            with open(ann_file, "r") as fa:
                articleNo = os.path.basename(ann_file).split("_")[0]
                ann_list = list()
                for line in fa:
                    if line.startswith("R") or line.startswith("#"):
                        continue
                    else:
                        try:
                            l = line.split()
                            ann_dict = {
                                    "segmentNo": l[0],
                                    "tag": l[1],
                                    "start": int(l[2]),
                                    "end": int(l[3]),
                                    "phrase": " ".join(l[4:]),
                                    "line_num": 0,
                                    "oneline": ""
                                    }
                        except ValueError:
                            print "file:" + ann_file

                        ann_list.append(ann_dict)

            for i, line in enumerate(oneline_list, start=1):
                for ann in ann_list:
                    if line["start"] <= ann["start"] and ann["end"] <= line["end"]:
                        ann["line_num"] = line["line_num"]
                        ann["oneline"] = line["oneline"]

            sorted_list =  sorted(ann_list, key=lambda x: x["line_num"])

            for k, group in itertools.groupby(sorted_list, key=lambda x: x["line_num"]):
                tag_list = list()
                oneline = ""
                for memb in group:
                    tag_list.append(memb["tag"])
                    oneline = memb["oneline"]
                if not k == 0:

                    if "Effect" in tag_list:
                        if "Target" in tag_list:
                            trg_eff.append((ann_article, k, oneline, tag_list))
                        else:
                            other.append((ann_article, k, oneline, tag_list))
        #for item in trg_eff:
        #    print item

        print "trg_eff:{}, other:{}".format(len(trg_eff), len(other))
        #for item in other:
        #    print item



if __name__ == "__main__":
    tag_collection(sys.argv[1])
    #for item in tag_collection(sys.argv[1]):
    #    print item


#python target_effect.py kirin
#python target_effect.py stewart
