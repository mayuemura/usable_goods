#PRF.py
#-*- coding: utf-8 -*-
#2016/02/08
#2016/02/14 modified

import sys


def main(log_file):

    with open(log_file, "r") as f:
        print log_file.split(".")[0].split("_")[-1]

        count = 0
        total_P = 0.0
        total_R = 0.0
        total_F1 = 0.0
        for line in f:
            if line.startswith("Macro-average precision,"):
                P, R, F1 = line.lstrip("Macro-average preision, recall, F1:(").rstrip(")\n").split(", ")
                count += 1
                total_P += float(P)
                total_R += float(R)
                total_F1 += float(F1)

        print "Precision:{}, Recall:{}, F1:{}".format(total_P/count, total_R/count, total_F1/count)

def except_zero(log_file):
    
    trg = {"P":0.0, "R":0.0, "F1":0.0, "count":0.0}
    eff = {"P":0.0, "R":0.0, "F1":0.0, "count":0.0}
    mou = {"P":0.0, "R":0.0, "F1":0.0, "count":0.0}
    o = {"P":0.0, "R":0.0, "F1":0.0, "count":0.0} 
    com = {"P":0.0, "R":0.0, "F1":0.0, "count":0.0}
    ver = {"P":0.0, "R":0.0, "F1":0.0, "count":0.0}

    acc = 0.0
    acc_cnt = 0

    with open(log_file, "r") as f:
        print log_file.split(".")[0].split("_")[-1]

        for line in f:
            if line.startswith("    ") and not line.endswith("******)\n"):
                tag, match, model, ref, precision, recall, F1 = line.strip(" \n").split(" ")
                try:
                    if tag.strip(":") == "O":
                        o["P"] += float(precision.strip("(,"))
                        o["R"] += float(recall.strip(","))
                        o["F1"] += float(F1.strip(")"))
                        o["count"] += 1

                    elif tag.strip(":").split("-")[1] == "Trg":
                        trg["P"] += float(precision.strip("(,"))
                        trg["R"] += float(recall.strip(","))
                        trg["F1"] += float(F1.strip(")"))
                        trg["count"] += 1

                    elif tag.strip(":").split("-")[1] == "Eff":
                        eff["P"] += float(precision.strip("(,"))
                        eff["R"] += float(recall.strip(","))
                        eff["F1"] += float(F1.strip(")"))
                        eff["count"] += 1

                    elif tag.strip(":").split("-")[1] == "MOU":
                        mou["P"] += float(precision.strip("(,"))
                        mou["R"] += float(recall.strip(","))
                        mou["F1"] += float(F1.strip(")"))
                        mou["count"] += 1

                    elif tag.strip(":").split("-")[1] == "Com":
                        com["P"] += float(precision.strip("(,"))
                        com["R"] += float(recall.strip(","))
                        com["F1"] += float(F1.strip(")"))
                        com["count"] += 1

                    elif tag.strip(":").split("-")[1] == "Ver":
                        ver["P"] += float(precision.strip("(,"))
                        ver["R"] += float(recall.strip(","))
                        ver["F1"] += float(F1.strip(")"))
                        ver["count"] += 1

                except IndexError:
                    print line
            elif line.startswith("Item accuracy"):
                acc += float(line.split(" ")[-1].strip("()\n"))
                acc_cnt += 1

    #今のところOタグはPRFに入れてない
    #2016/02/16 Trgもはずす

    #print "O    precision:{}, recall:{}, F1:{}".format(o["P"]/o["count"], o["R"]/o["count"], o["F1"]/o["count"]) 
    #print "Trg  precision:{}, recall:{}, F1:{}".format(trg["P"]/trg["count"], trg["R"]/trg["count"], trg["F1"]/trg["count"])


    print "accuracy:{}".format(acc/acc_cnt)
    print "Eff  precision:{}, recall:{}, F1:{}".format(eff["P"]/eff["count"], eff["R"]/eff["count"], eff["F1"]/eff["count"])
    print "MOU  precision:{}, recall:{}, F1:{}".format(mou["P"]/mou["count"], mou["R"]/mou["count"], mou["F1"]/mou["count"])
    print "Com  precision:{}, recall:{}, F1:{}".format(com["P"]/com["count"], com["R"]/com["count"], com["F1"]/com["count"])
    print "Ver  precision:{}, recall:{}, F1:{}".format(ver["P"]/ver["count"], ver["R"]/ver["count"], ver["F1"]/ver["count"])

    P = eff["P"] + mou["P"] + trg["P"] + com["P"] + ver["P"]
    R = eff["R"] + mou["R"] + trg["R"] + com["R"] + ver["R"]
    F1 = eff["F1"] + mou["F1"] +trg["F1"] + com["F1"] + ver["F1"]
    count = eff["count"] + mou["count"] + trg["count"] + com["count"] + ver["count"]

    print "all  P:{}, R:{}, F1:{}".format(P/count, R/count, F1/count)

        #print trg["P"]


if __name__ == "__main__":
    #main(sys.argv[1])
    except_zero(sys.argv[1])

#python PRF.py log_file
