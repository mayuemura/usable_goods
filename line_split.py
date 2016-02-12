#line_split.py
#-*-coding:utf-8 -*-
#2016/02/05

import sys

def main(dirname):
    sentence = list()

    with open("train_"+dirname, "r") as fr, open("train"+dirname.upper(), "w") as fw:
        for line in fr:
            BIO, word, POS = line.split("\t")
            if (word[0].isupper()) and (BIO[0] != "I"):
                fw.write("\n"+line)
            else:
                fw.write(line)

if __name__ == "__main__":
    main(sys.argv[1])
