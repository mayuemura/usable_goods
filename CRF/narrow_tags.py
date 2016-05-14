# narrow_tags.py
#  -*- coding:utf-8 -*-
# 2016/02/09
# train, testデータのlabelをEffect, MOU, Targetだけにする
# 2016/02/16 modified (Trgも予測の対象から外す)
# 2016/03/?? modified (Effect, MOU, Composed, Verを予測)

import sys

def main(data_file):

    # 取り除きたいタグ
    label_set = {
            "B-Trg",
            "I-Trg",
            "B-Cer",
            "I-Cer",
            "B-Deg",
            "I-Deg",
            "B-Null",
            "I-Null",
            "B-Part",
            "I-Part",
            "B-Loc",
            "I-Loc",
            "B-Time",
            "I-Time",
            "B-User",
            "I-User",
            }


    with open(data_file, "r") as fr, open(data_file+"_narrowed", "w") as fw:
        for line in fr:
            if line == "\n" or line.startswith("#"):
                fw.write(line)
            else:
                BIO, word, POS, NER = line.split("\t")
                if BIO in label_set:
                    fw.write("{}\t{}\t{}\t{}".format("O", word, POS, NER))
                else:
                    fw.write(line)

if __name__ == "__main__":
    main(sys.argv[1])

#python narrow_tags.py train
