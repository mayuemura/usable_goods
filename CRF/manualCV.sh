#!/bin/bash

# manual 10_fold cross_validation

# 1
cat	NS_02 NS_03 NS_04 NS_05 NS_06 NS_07 NS_08 NS_09 NS_10 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_01 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result01

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result01 | awk -F"\t" {'print $1'} > gold

cat manualCV_result01 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 2
cat	NS_03 NS_04 NS_05 NS_06 NS_07 NS_08 NS_09 NS_10 NS_01 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_02 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result02

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result02 | awk -F"\t" {'print $1'} > gold

cat manualCV_result02 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 3
cat	NS_04 NS_05 NS_06 NS_07 NS_08 NS_09 NS_10 NS_01 NS_02 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_03 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result03

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result03 | awk -F"\t" {'print $1'} > gold

cat manualCV_result03 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 4
cat	NS_05 NS_06 NS_07 NS_08 NS_09 NS_10 NS_01 NS_02 NS_03 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_04 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result04

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result04 | awk -F"\t" {'print $1'} > gold

cat manualCV_result04 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 5
cat	NS_06 NS_07 NS_08 NS_09 NS_10 NS_01 NS_02 NS_03 NS_04 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_05 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result05

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result05 | awk -F"\t" {'print $1'} > gold

cat manualCV_result05 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 6
cat	NS_07 NS_08 NS_09 NS_10 NS_01 NS_02 NS_03 NS_04 NS_05 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_06 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result06

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result06 | awk -F"\t" {'print $1'} > gold

cat manualCV_result06 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log

# 7
cat	NS_08 NS_09 NS_10 NS_01 NS_02 NS_03 NS_04 NS_05 NS_06 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_07 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result07

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result07 | awk -F"\t" {'print $1'} > gold

cat manualCV_result07 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 8
cat	NS_09 NS_10 NS_01 NS_02 NS_03 NS_04 NS_05 NS_06	NS_07 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_08 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result08

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result08 | awk -F"\t" {'print $1'} > gold

cat manualCV_result08 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 9
cat	NS_10 NS_01 NS_02 NS_03 NS_04 NS_05 NS_06 NS_07 NS_08 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_09 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result09

# strict
#cat manualCV_result | python conlleval.py >> result.txt

# lenient
cat manualCV_result09 | awk -F"\t" {'print $1'} > gold

cat manualCV_result09 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# 10
cat NS_01 NS_02 NS_03 NS_04 NS_05 NS_06 NS_07 NS_08 NS_09 | ./feature.py > manualCV_train.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m manualCV.model manualCV_train.f

./feature.py < NS_10 > manualCV_test.f

~okazaki/local/bin/crfsuite tag -r -m manualCV.model < manualCV_test.f > manualCV_result10

# strict
cat manualCV_result10 | python conlleval.py >> result.txt

# lenient
cat manualCV_result10 | awk -F"\t" {'print $1'} > gold

cat manualCV_result10 | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> lenient_log


# lenient_avg
python lenient_avg.py lenient_log >> result.txt

rm lenient_log

