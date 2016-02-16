#FB_relation_grep.py
#-*- coding:utf-8 -*-
#2016/02/16

import sys
from pymongo import Connection

client = Connection("beer")


def relation_grep(FB_files):

    with open("Freebase/except_relation", "r") as fr, open("Freebase/except_value", "r") as fv:
        except_relation = set(fr.read().split("\n"))
        except_value = set(fv.read().split("\n"))

    with open("Freebase/relation_pattern", "r") as f:
        relation_pattern = set(f.read().split("\n"))
    
    for FB_file in FB_files:
        value_set = set()
        with open(FB_file, "r") as f:
            for line in f:
                entity, relation, value = line.rstrip("\t.\n").split("\t")
                #if relation in except_relation or value in except_value:
                #    continue
                #else
                #    print line.rstrip("\n")
                if relation in relation_pattern:
                    value_set.add(value)


if __name__ == "__main__":
    relation_grep(sys.argv[1:])

#python FB_relation_grep.py [FB_file]
