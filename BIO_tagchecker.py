#BIO_tagchecker.py
#-*- coding:utf-8 -+\*-
#2016/02/02
#BIOラベルの数が正しいか調べる
import sys


def tagchecker(dirname):
    biofile = "BIO_{}.txt".format(dirname)

    with open(biofile, "r") as f:
        count = 0
        article = 1
        for line in f:
            tag = line.split("\t")
            if len(tag) > 1 and tag[1].startswith("B"):
                count += 1
            elif line == "\n":
                print article, count
                count = 0
                article += 1

if __name__ == "__main__":
    tagchecker(sys.argv[1])
