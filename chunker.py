#chunker.py
#-*- coding;utf-8 -*-
#2016/02/17


import glob
import sys
from lxml import etree

def chunker(dirname):

    xml_filelist = glob.glob("stanford-corenlp-full-2015-12-09/xml_out/{}/*.txt.out".format(dirname))
    xml_filelist.sort()

    for xml_file in xml_filelist:

        with open(xml_file, "r") as f:
            root = etree.parse(f)
            chunking = root.xpath("/root/document/semtemces/sentence")
            print chunking

if __name__ == "__main__":
    chunker(sys.argv[1])

#python chunker.py cosme
