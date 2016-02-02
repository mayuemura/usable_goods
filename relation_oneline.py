#relation_oneline.py
#-*- coding: utf-8 -*-
#2016/01/22

import glob
import itertools
import os.path
import sys

def tag_collection(annotator):

    #relationが1文中に収まっているかどうか
    true_list = list()
    false_list = list()

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

            #if txt_file == "data/health/txt/07_Antioxidant.txt":
            #    for item in oneline_list:
            #        print item

            with open(ann_file, "r") as fa:
                articleNo = os.path.basename(ann_file).split("_")[0]
                ann_list = list()
                rel_list = list()
                for line in fa:
                    if line.startswith("#"):
                        continue
                    elif line.startswith("R"):
                        l = line.split()
                        rel_dict = {
                                "relationNo": l[0],
                                "tag": l[1],
                                "arg1": l[2].split(":")[1],
                                "arg2": l[3].split(":")[1],
                                "range": [0, 0, 0, 0],  #relationの始まりと終わりを入れる
                                "oneline": False
                                }
                        for ann in ann_list:
                            if rel_dict["arg1"] == ann["segmentNo"]:
                                rel_dict["range"][0:2] = ann["start"], ann["end"]

                            if rel_dict["arg2"] == ann["segmentNo"]:
                                rel_dict["range"][2:4] = ann["start"], ann["end"]
                        rel_list.append(rel_dict)
                    else:
                        try:
                            m = line.split()
                            ann_dict = {
                                    "segmentNo": m[0],
                                    "tag": m[1],
                                    "start": int(m[2]),
                                    "end": int(m[3]),
                                    "phrase": " ".join(m[4:]),
                                    "line_num": 0,  #今回は関係ない
                                    "oneline": ""   #今回は関係ない
                                    }
                        except ValueError:
                            print "file:" + ann_file
                        ann_list.append(ann_dict)

            #確認用
            #if not rel_list == []:
            #    print ann_article, rel_list

            #各行にrelationの最初と最後が含まれてるかを判断
            if not rel_list == []:
                for rel in rel_list:

                    for line in oneline_list:
                        #print line["start"], line["end"]
                        if line["start"] <= min(rel["range"]) and max(rel["range"]) <= line["end"]:
                            rel["oneline"] = rel["oneline"] or True
                    
                    
                        #if txt_file == "data/health/txt/07_Antioxidant.txt":
                        #    print line

                #1文に収まっていればtrue
                for rel in rel_list:
                    if rel["oneline"] == True:
                        true_list.append((ann_article, rel))
                    else:
                        false_list.append((ann_article, rel))

                #if txt_file == "data/health/txt/07_Antioxidant.txt":
                #    print rel_list


    #詳細確認用（kirin/stewart_relation.txtに保存済み）
    for t in true_list:
        print t

    print "\n"
    for f in false_list:
        print f

    t = len(true_list)
    f = len(false_list)
    per = t*1.0/(t+f) * 100
    print "true:{}, false:{}, true_%:{}".format(t, f, per)


if __name__ == "__main__":
    tag_collection(sys.argv[1])
    #for item in tag_collection(sys.argv[1]):
    #    print item


#python relation_oneline.py kirin
#python relation_oneline.py stewart
