#new_annfile.py
#-*- coding:utf-8 -*-
#2016/01/29

import sys
import glob
import os

def main(dirname):
    txtfiles = glob.glob(dirname+"/*.txt")
    for txtfile in txtfiles:
        annfile = txtfile.split("/")[-1].split(".")[0] + ".ann"

        #入力が/含んでも含まなくても大丈夫なように
        if dirname.endswith("/"):
            path = dirname+annfile
        else:
            path = dirname+"/"+annfile

        with open(dirname+"/"+annfile, "w") as _:
            pass

if __name__ == "__main__":

    main(sys.argv[1])
    #for i in main(sys.argv[1]):
    #    print i

#python new_annfile.py public_html/..../cosme/deepika
