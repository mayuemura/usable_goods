#number_of_features.py
#-*- coding:utf-8 -*-
#2016/03/01

import sys

def main(logfile):

    feature = 0
    cnt = 0
    with open(logfile, "r") as f:
        for line in f:
            if line.startswith("Number of features"):
                feature += int(line.strip("\n").split(" ")[-1])
                cnt += 1

    return feature*1.0/cnt


if __name__ == "__main__":
    print main(sys.argv[1])

#python number_of_features.py log_file_10.txt
