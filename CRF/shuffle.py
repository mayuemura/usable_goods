# shuffle.py
# -*- coding:utf-8 -*-
# 2016/05/15
# cosme-->health-->...のtrainの中身を記事ごとにバラバラに並び替える
# 大きいデータで使わない

import random
import sys

def shuffle(txt):

    #TODO メモリに全部載せるので大きいデータは注意
    with open(txt, "r") as f:
        data = f.read()

    snippets = data.lstrip("#").split("\n\n#")
    #print snippets

    random.shuffle(snippets)

    for snippet in snippets:
        print "#" + snippet + "\n\n"

if __name__ == "__main__":

    shuffle(sys.argv[1])

# python shuffle.py train_narrowed
