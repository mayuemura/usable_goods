#five_lines.py
#-*- coding:utf-8 -*-
#2015/12/01

import glob
import os.path
import sys


def main(input_dir, output_dir):

    for txtfile in glob.glob(input_dir+"/*.txt"):

        with open(txtfile, "r") as fi:
            lines_list = list()

            for line in fi:
                l = line.replace(".", ".\n")
                lines_list.extend(l.split("\n"))

            if "\n" in lines_list:
                lines_list.remove("\n")

            if len(lines_list) < 6:
                pass
            else:
                with open(output_dir + "/" + os.path.basename(txtfile), "w") as fo:
                    fo.writelines(lines_list[:5])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])


#python data/health/orita data/health/uemura
