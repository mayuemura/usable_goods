#FB_wikicopipe.py
#-*- coding:utf-8 -*-
#2016/02/28
#Freebaseで検索したもののうちwikiを引用してるだけのやつをだす


import glob
import sys


def main():

    wiki_cnt = 0
    groups = ["cosme", "health", "nlp2016"]

    for group in groups:
        for fb in glob.glob("Freebase/{}_*.txt".format(group)):
            with open(fb, "r") as f:
                txt = f.read()
                if txt == "":
                    wiki_cnt += 1
    return wiki_cnt

if __name__ == "__main__":
    print main()

#python FB_wikicopipe.py
