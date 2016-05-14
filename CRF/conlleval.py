#!/usr/bin/env python

import sys
import os

fo = os.popen('perl /home/okazaki/ict/bin/conlleval.pl', 'w')

for line in sys.stdin:
    line = line.strip('\n')
    if line:
        fo.write('a\t%s\n' % line)
    else:
        fo.write('\n')

