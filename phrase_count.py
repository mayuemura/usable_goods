#phrase_count.py
#-*- coding:utf-8 -*-
#2016/02/22

import sys
import itertools

def main(annotated_file):

    d = dict()
    with open(annotated_file, "r") as f:
        for k, g in itertools.groupby(sorted(f.read().split("\n")), key=lambda x: x.split("\t")[0]):
            if k.startswith("#") or k == "":
                continue
            else:
                d[k] = len(list(g))

    total = sum(d.values())
    print total
    for k, v in d.iteritems():
        print "{}\t{}\t{}%".format(k, v, round(v*1.0/total*100,2))

if __name__ == "__main__":
    main(sys.argv[1])


#python phrase_count.py [filename]
#VPとかのやつ
