#lenient_F.py
#-*- coding:utf-8 -*-
#2016/02/28 とりあえず記号なしで
#2016/03/04 lenient
#2016/03/05 Trgのぞくには、labelsから外して78行目からのif文を実行

import itertools
import numpy as np
import sys


def main():
    DP = "trainDP_stripsharp"
    ST = "trainST"

    with open(DP, "r") as dp, open(ST, "r") as st:
        BIO_dp = list()
        BIO_st = list()
        
        for line in dp:
            if line.startswith("#"):
                continue
            elif line == "\n":
                BIO_dp.append("")
            else:
                BIO_dp.append(line.split("\t")[0])

        for line in st:
            if line == "\n":
                BIO_st.append("")
            else:
                BIO_st.append(line.split("\t")[0])
        

        for d, s in itertools.izip(BIO_dp, BIO_st):
            print "{}\t{}".format(d, s)
        #    if (not d == "") and (not s == ""):
        #        print d.split("\t")[1], s.split("\t")[1]

    #print len(BIO_dp), len(BIO_st)


def lenient_F(gold, system):


    labels = [
            #"Trg",
            "Ver",
            "Eff",
            "MOU",
            #"Cer",
            #"Deg",
            #"Null",
            "Com",
            #"Part",
            #"Loc",
            #"Time",
            #"User",
            "O"
            ]
    label_num = len(labels)
    mtrx = np.zeros((label_num, label_num))

    with open(gold, "r") as g, open(system, "r") as s:
        for line_g, line_s in itertools.izip(g, s):
            if line_g == "\n" or line_s == "\n":
                continue
            else:
                label_gold = line_g.strip("\n").split("\t")[0]
                label_system = line_s.strip("\n").split("\t")[0]


                if not label_gold == "O":
                    label_gold = label_gold.split("-")[1]
                if not label_system == "O":
                    label_system = label_system.split("-")[1]


                #みたくないラベルを無視
                if not label_gold in labels:
                    #label_gold = "O"
                    continue
                if not label_system in labels:
                    #label_system = "O"
                    continue



                index_gold = labels.index(label_gold)
                index_system = labels.index(label_system)

                mtrx[index_system, index_gold] += 1

    #print mtrx
    #"""
    true_negative = mtrx[-1,-1]
    ALL_tp = 0
    ALL_fp = 0
    ALL_fn = 0

    macro_P = 0
    macro_R = 0
    macro_F1 = 0
    cnt = 0

    for label in labels:
        indx = labels.index(label)
        false_positive = 0
        false_negative = 0

        for i in range(label_num):
            if indx == i:
                true_positive = mtrx[indx, indx]

            else:
                false_positive += mtrx[indx, i]
                false_negative += mtrx[i, indx]


        P_denominator = true_positive + false_positive
        R_denominator = true_positive + false_negative

        if not true_positive == 0:
            precision = true_positive / (true_positive + false_positive)
            recall = true_positive / (true_positive + false_negative)
            F1 = 2*precision*recall / (precision + recall)
            #yield "{}\nprecision:{} recall:{} F1:{}".format(label, precision, recall, F1)
            macro_P += precision
            macro_R += recall
            macro_F1 += F1
            cnt += 1
        else:
            continue

        ALL_tp += true_positive
        ALL_fp += false_positive
        ALL_fn += false_negative


    micro_P = ALL_tp / (ALL_tp + ALL_fp)
    micro_R = ALL_tp / (ALL_tp + ALL_fn)
    micro_F1 = 2*micro_P*micro_R / (micro_P + micro_R)
    yield "micro_avg precision:{} recall:{} F1:{}".format(micro_P, micro_R, micro_F1)
    yield "macro_avg precision:{} recall:{} F1:{}".format(macro_P/cnt, macro_R/cnt, macro_F1/cnt)

def macro_avg(log_file):
    FLAG = 0.0
    cnt = 0
    F1 = 0
    with open(log_file, "r") as f:
        for line in f:
            if FLAG == 0 and line == "macro_avg\n":
                FLAG = 1
            elif FLAG == 1:
                F1 += float(line.strip("\n").split(" ")[-1].split(":")[1])
                cnt += 1
                FLAG = 0

        return F1/cnt
    #"""
if __name__ == "__main__":
    #main()
    for item in lenient_F(sys.argv[1], sys.argv[2]):
        print item

    #print macro_avg(sys.argv[1])
    #lenient_F(sys.argv[1], sys.argv[2])

#python annotatorF.py gold system
