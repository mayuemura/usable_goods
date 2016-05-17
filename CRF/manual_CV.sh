#!/bin/bash

# manual 10_fold cross_validation

# 1

cat	NS_02 NS_03 NS_04 NS_05 NS_06 NS_07 NS_08 NS_09 NS_10 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_01 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result

# strict
cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result | awk -F"\t" {'print $1'} > gold

cat manualCV_result | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> result.txt


