#insert_signs.py
#-*- coding:utf-8 -*-
#2016/02/23

import itertools
import sys


def main():
    
    signs = {".", ",", "``", "''", "(", ")", "|", "#", "--", ";", ":"}

    with open("trainDP_lmtd", "r") as dp, open("trainST_lmtd", "r") as st:
        dp_lines = dp.read().split("\n")
        st_lines = st.read().split("\n")

    new_st_lines = list()
    #print dp_lines[-4:-1]
    #print st_lines[-4:-1]
    #print len(st_lines), len(dp_lines)
    #"""
    for _ in range(len(dp_lines)):
        st_line = st_lines.pop(0)
        dp_line = dp_lines.pop(0)

        try:
            if (dp_line.startswith("#") or dp_line == "") and (st_line.startswith("#") or st_line == ""):
                new_st_lines.append(st_line)
                #print st_line + "\t" + dp_line

            elif st_line.startswith("#") or st_line == "":
                new_st_lines.append(dp_line)
                new_st_lines.append("")
                dp_lines.pop(0)
                #print st_line + "\t" + dp_line

            elif st_line.split("\t")[1] == dp_line.split("\t")[1]:
                new_st_lines.append(st_line)
                #print st_line + "\t" + dp_line

            else:
                new_st_lines.append(dp_line)
                #print st_line + "\t" + dp_line
                dp_lines.pop(0)
        except IndexError:
            #for new_line in new_st_lines:
            #    print new_line
            print "Error!\t[{}]\t[{}]".format(st_line,dp_line)
            break
        #    new_st_lines.append(st_line)
        #    dp_lines.pop(0)
        #else:
        #    new_st_lines.append(dp_lines.pop(0))
    #"""
    #print len(new_st_lines)

    for new_line in new_st_lines:
        print new_line


if __name__ == "__main__":
    main()

    
#python insert_signs.py
