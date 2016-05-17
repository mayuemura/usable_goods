#!/bin/bash

# hold out

./feature.py < train_NS > train_NS.f

~okazaki/local/bin/crfsuite learn -a ap -p max_iterations=20 -m HO.model train_NS.f

./feature.py < test_NS > test_NS.f

# strict
~okazaki/local/bin/crfsuite tag -r -m HO.model < test_NS.f | conlleval.py >> result.txt

# lenitne
~okazaki/local/bin/crfsuite tag -r -m HO.model < test_NS.f > HO_result

cat HO_result | awk -F"\t" {'print $1'} > gold

cat HO_result | awk -F"\t" {'print $2'} > system

python lenient_F.py gold system >> result.txt

