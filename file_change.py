#-*- coding:utf-8 -*-
#file_change.py
#2015/11/20
#2016/01/04

import glob
import os
import os.path
import sys
import shutil
import re

"""
def file_change(file_names):
	dir_name = os.path.dirname(file_names[0]) + "/"
        #dir_name = "data/health/hinan/"
	for i, file_name in enumerate(file_names, start=1):
                base = os.path.basename(file_name)
		txt_file_name = dir_name + str(i).zfill(3) + "_" + re.sub(r"[0-9]+_", "", base)
		ann_file_name = txt_file_name.replace("txt", "ann")

		shutil.copyfile(file_name, txt_file_name)

		with open(ann_file_name, "w") as f:
			pass

        #os.system("rm "+dir_name+"0*")
"""

def file_numbering(dirname):
    #すでにディレクトリにある番号を見てからナンバリングする
    #annファイルもつくる
    
    
    txtfiles = sorted(glob.glob(dirname+"/*.txt"))
    for txtfile in txtfiles:
        basename = txtfile.lstrip(dirname+"/")
        if basename[:3].isdigit():
            number = int(basename[:3])
        else:
            number += 1
            num_txtfile = dirname+"/"+str(number).zfill(3)+"_"+basename
            num_annfile = num_txtfile.replace("txt", "ann")

            shutil.copyfile(txtfile, num_txtfile)

            with open (num_annfile, "w") as _:
                pass

            os.system("rm "+txtfile)


if __name__ == "__main__":
    file_numbering(sys.argv[1])

#cp [originaldata] data/[dir]
#python file_change.py data/cosme/*.txt
