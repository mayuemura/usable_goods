#!/bin/bash

#leave_one_out cross_validation
./feature.py < train_lmtd > train_lmtd.f

~okazaki/local/bin/crfsuite learn -a ap -g5 -x -p max_iterations=20 train_lmtd.f > log_file_5.txt

python PRF.py log_file_5.txt

~okazaki/local/bin/crfsuite learn -a ap -g10 -x -p max_iterations=20 train_lmtd.f > log_file_10.txt

python PRF.py log_file_10.txt

#~okazaki/local/bin/crfsuite learn -a ap -g387 -x -p max_iterations=20 train_lmtd.f > log_file_387.txt

python PRF.py log_file_387.txt

#./feature.py < splt_train_lmtd > splt_train_lmtd.f

#~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m emt.model splt_train_lmtd.f

#./feature.py < splt_test_lmtd > splt_test_lmtd.f

#~okazaki/local/bin/crfsuite tag -r -m emt.model < splt_test_lmtd.f | conlleval.py >> result.txt

