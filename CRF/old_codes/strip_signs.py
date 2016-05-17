#strip_signs.py
#-*-coding:utf-8 -*-
#2016/02/23

import sys


def main(filename):

    signs = {".",",", "''", "``", "(", ")", "|", "#", "--", ";", ":"}

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            elif line == "\n":
                print ""
            else:
                if line.split("\t")[1] in signs:
                    continue
                else:
                    print line.strip("\n")


if __name__ == "__main__":
    main(sys.argv[1])

#python strip_signs.py [filename]
