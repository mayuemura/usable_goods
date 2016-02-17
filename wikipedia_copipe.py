#wikipedia_copipe.py
#-*- coding:utf-8 -*-
#2016/02/16

import sys

def main(relation_file):

    wikipedia = 0
    rel_number = set()

    with open(relation_file, "r") as f:
        for line in f:
            if line.startswith("Freebase") or line.startswith("{"):
                if len(rel_number) > 0 and max(rel_number) == 0:
                    wikipedia += 1
                else:
                    rel_number = set()
            elif not line == "\n":
                try:
                    rel_number.add(int(line.split("\t")[1]))
                except IndexError:
                    print line
    print wikipedia

if __name__ == "__main__":
    main(sys.argv[1])


#python wikipedia_copipe.py Freebase/FB_cosme_relation.txt
