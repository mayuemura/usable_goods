#data_formatw.py
#-*- coding: utf-8 -*-
#2015/12/16

import glob
import itertools
import os.path
import re
import sys

strip_ptrn = re.compile(r"[^a-zA-Z0-9]|CAS")

def data_formate(dirname):

    pos_list = list()
    with open(dirname+"/POS.txt", "r") as POS:
        for line in POS:
            word = line.lstrip("#|:''\"``")

            if strip_ptrn.match(word):
                continue
            else:
                pos_list.append(word)
    
    bio_list = list()
    with open(dirname+"/BIO.txt", "r") as BIO:
        for line in BIO:
            word = line.lstrip("#|:''\"``")

            if strip_ptrn.match(word):
                continue
            else:
                bio_list.append(word)

    for  p_elem, b_elem in itertools.izip(pos_list, bio_list):
        try:
            word_p, pos = p_elem.split("\t")
            word_b, bio = b_elem.split("\t")

        except ValueError:
            print word_p, pos
            print word_b, bio
            break

        if word_p.strip("\"):;.") == word_b.rstrip("\");:."):
            print "{}\t{}\t{}".format(bio.rstrip("\n"), word_p, pos.rstrip("\n"))

        else:
            print "error!", word_p, word_b


if __name__ == "__main__":
    #remove_NotAgree(sys.argv[1])
    data_formate(sys.argv[1])

#python deta_formate.py cosme
