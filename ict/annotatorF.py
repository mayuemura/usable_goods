#annotatorF.py
#-*- coding:utf-8 -*-
#2016/02/28 とりあえず記号なしで

import itertools
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

if __name__ == "__main__":
    main()

#python annotatorF.py
