#postag.py
#-*- coding:utf-8 -*-
#2015/12/17

import glob
import sys

from lxml import etree

def postag(dirname):

    xml_filelist = glob.glob(dirname + "/xml_out/*")
    xml_filelist.sort()

    for xml_file in xml_filelist:

        with open(xml_file, "r") as f:
            root = etree.parse(f)
            tokens = root.xpath("/root/document/sentences/sentence/tokens/token")

            for token in tokens:
                word = token.find("word").text
                pos = token.find("POS").text
                yield "{}\t{}".format(word, pos)


if __name__ == "__main__":
    for pair in postag(sys.argv[1]):
        print pair
