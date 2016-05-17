#!/bin/bash

#leave_one_out cross_validation
./feature.py < train_narrowed > train_narrowed.f

~okazaki/local/bin/crfsuite learn -a ap -g2 -x -p max_iterations=20 train_narrowed.f > log2.txt
python PRF.py log2.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g3 -x -p max_iterations=20 train_narrowed.f > log3.txt
python PRF.py log3.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g4 -x -p max_iterations=20 train_narrowed.f > log4.txt
python PRF.py log4.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g5 -x -p max_iterations=20 train_narrowed.f > log5.txt
python PRF.py log5.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g6 -x -p max_iterations=20 train_narrowed.f > log6.txt
python PRF.py log6.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g7 -x -p max_iterations=20 train_narrowed.f > log7.txt
python PRF.py log7.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g8 -x -p max_iterations=20 train_narrowed.f > log8.txt
python PRF.py log8.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g9 -x -p max_iterations=20 train_narrowed.f > log9.txt
python PRF.py log9.txt >> result.txt

~okazaki/local/bin/crfsuite learn -a ap -g793 -x -p max_iterations=20 train_narrowed.f > log793.txt
python PRF.py log793.txt >> result.txt

