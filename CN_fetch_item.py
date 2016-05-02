#CN_fetch_item.py
#-*- coding:utf-8 -*-
#2016/02/28

import glob
import os
import sys

def fetch_item(dirname):

    with open("data/{}/keyword.txt".format(dirname), "r") as f:
        for line in f:
            articleNo, Target = line.strip("\n").split("\t")
            target = Target.lower().replace(" ", "_")
            os.system("grep '/c/en/{}/' CN5.txt > ConceptNet/{}_{}_{}.txt".format(target, dirname, articleNo, target))

if __name__ == "__main__":
    fetch_item(sys.argv[1])


#python CN_fetch_item.py cosme
