#line_split.py
#-*-coding:utf-8 -*-
#2016/02/05

import sys
import glob

from pymongo import Connection


def give_Target(dirname):

    client = Connection("beer")
    db = client["usable_goods_SD"]
    coll = db[dirname]

    nums = coll.distinct("articleNo")

    Target_list = list()
    for num in nums:
        Target_list.append(",".join(coll.find({"articleNo":num, "annotator":"dp", "dp_tag":"Target"}).distinct("words")))

    #TODO fr一般化
    prev = ""
    with open("log", "r") as fr, open("trainDP"+dirname, "w") as fw:
        for line in fr:
            if line.startswith("#"):
                fw.write("\n#\t{}\n".format(Target_list.pop(0)))
                prev = ""
                #print "#\t{}".format(Target_list.pop(0))
            elif line == "\n":
                continue
            else:
                BIO, word, POS = line.split("\t")
                if (word[0].isupper()) and (BIO[0] != "I") and (prev == "."):
                    fw.write("\n"+line)
                    prev = word
                    #print "\n"+line
                else:
                    fw.write(line)
                    prev = word
                    #print line

if __name__ == "__main__":
    give_Target(sys.argv[1])


#python line_split.py cosme
