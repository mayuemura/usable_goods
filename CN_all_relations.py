#CN_all_relations.py
#-*- coding:utf-8 -*-

import sys

def main():
    relations = set()
    with open("conceptnet5.1b-20120501.csv", "r") as fi, open("ConceptNet/relations.txt", "w") as fo:
        for line in fi:
            relations.add(line.split("/")[4]+"\n")

        fo.writelines(relations)

if __name__ == "__main__":
    main()

#python CN_all_relations.py
