#CN_relation.py
#-*- coding:utf-8 -*-
#2016/02/28

import glob
import re
import sys

groups = ["cosme", "health", "nlp2016"]
rel_ptrn = re.compile(r"/a/\[/r/([A-Za-z]*?)/")

def main():

    null_cnt = 0
    rel_set = set()

    for group in groups:
        for cn in glob.glob("ConceptNet/{}_*.txt".format(group)):
            with open(cn, "r") as f:
                txt = f.read()
                if txt == "":
                    null_cnt += 1
                else:
                    line_list = txt.split("\n")
                    for line in line_list:
                        mtch =  rel_ptrn.match(line.split(",")[0])
                        if mtch:
                            rel_set.add(mtch.group(1))

    return null_cnt, rel_set


Effect_rel = {
        "CausesDesire",
        "UsedFor",
        "Entails",
        "CapableOf",
        "HasSubevent",
        "Causes",
        "HasFirstSubevent",
        "HasLastSubevent"
        }


def relation_grep():

    for group in groups:
        for cn in sorted(glob.glob("ConceptNet/{}_*.txt".format(group))):
            with open(cn, "r") as f:
                cnt = 0
                txt = f.read()
                if txt == "":
                    continue
                else:
                    line_list = set(txt.split("\n"))
                    for line in line_list:
                        mtch =  rel_ptrn.match(line.split(",")[0])
                        if mtch:
                            rel = mtch.group(1)

                            if rel in Effect_rel:
                                cnt += 1
            if not cnt == 0:    #これを外すとinstanceがあるすべてのアイテムを表示(71)
                yield cn, cnt



if __name__ == "__main__":
    #print main()

    total = 0
    cnt = 0
    for result in relation_grep():
        total += result[1]
        cnt += 1
    print total, cnt
    #relation_grep()


#python CN_relation.py
