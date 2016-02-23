#!/usr/bin/env python

import sys

#from nltk.stem.wordnet import WordNetLemmatizer
#lmtzr = WordNetLemmatizer()


def readiter(fi, names=('y', 'w', 'pos'), sep='\t'):
    seq = []
    for line in fi:
        line = line.strip('\n')
        if not line:
            yield seq, target_set
            seq = []
        elif line.startswith("#"):
            target_set = set(line.lstrip("#\t").split(","))
        else:
            fields = line.split(sep)
            if len(fields) != len(names):
                raise ValueError(
                    'Each line must have %d fields: %s\n' % (len(names), line))
            seq.append(dict(zip(names, tuple(fields))))

def apply_template(seq, t, template):
    name = '|'.join(['%s[%d]' % (f, o) for f, o in template])
    values = []
    for field, offset in template:
        p = t + offset
        if p not in range(len(seq)):
            return None
        values.append(seq[p][field])
    return '%s=%s' % (name, '|'.join(values))

def escape(src):
    return src.replace(':', '__COLON__')

if __name__ == '__main__':
    fi = sys.stdin
    fo = sys.stdout
    readiter(fi)

    templates = []
    templates += [(('w', i),) for i in range(-3, 4)]
    templates += [(('w', i), ('w', i+1)) for i in range(-3, 3)]

    templates += [(('pos', i),) for i in range(-3, 4)]
    templates += [(('pos', i), ('pos', i+1)) for i in range(-3, 3)]
    templates += [(('pos', i), ('pos', i+1), ('pos', i+2)) for i in range(-3, 3)]

    #templates += [(('chk', i),) for i in range(-2, 3)]
    #templates += [(('chk', i), ('chk', i+1)) for i in range(-2, 2)]

    templates += [(('iu', i),) for i in range(-3, 4)]
    templates += [(('iu', i), ('iu', i+1)) for i in range(-3, 3)]

    #word_lowercase
    templates += [(('wl', i),) for i in range(-3, 4)]
    templates += [(('wl', i), ('wl', i+1)) for i in range(-3, 3)]
    #templates += [(('wl', i), ('wl', i+1), ('wl', i+2)) for i in range(-3, 3)]

    #target
    templates += [(('tr', i),) for i in range(-3, 4)]
    templates += [(('tr', i), ('tr', i+1)) for i in range(-3, 3)]
    #templates += [(('tr', i), ('tr', i+1), ('tr', i+2)) for i in range(-3, 3)]


    #target_pattern
    templates += [(('tr', i), ('wl', i+1)) for i in range(-3, 3)]
    templates += [(('tr', i), ('wl', i+1), ('wl', i+2)) for i in range(-3, 3)]
    templates += [(('tr', i), ('wl', i+1), ('wl', i+2), ('wl', i+3)) for i in range(-3, 3)] 
    templates += [(('tr', i), ('wl', i+1), ('wl', i+2), ('wl', i+3), ('wl', i+4)) for i in range(-3, 3)]
    

    templates += [(('tr', i), ('pos', i+1)) for i in range(-3, 3)]
    templates += [(('tr', i), ('pos', i+1), ('pos', i+2)) for i in range(-3, 3)]
    templates += [(('tr', i), ('pos', i+1), ('pos', i+2), ('pos', i+3)) for i in range(-3, 3)]
    templates += [(('tr', i), ('pos', i+1), ('pos', i+2), ('pos', i+3), ('pos', i+4)) for i in range(-3, 3)]
    templates += [(('pos', i), ('wl', i)) for i in range(-3, 3)]
    templates += [(('pos', i), ('pos', i+1), ('wl', i), ('wl', i+1)) for i in range(-3, 3)]
    templates += [(('pos', i), ('pos', i+1), ('pos', i+2), ('wl', i), ('wl', i+1), ('wl', i+2)) for i in range(-3, 3)]

 
    #disease_gazetteer
    templates += [(('di', i),) for i in range(-3, 4)]
    templates += [(('di', i), ('di', i+1)) for i in range(-3, 3)]

    #bool(POS is 'TO') and following POS
    templates += [(('pt', i), ('pos', i+1)) for i in range(-3, 3)]
    templates += [(('pt', i), ('pos', i+1), ('pos', i+2)) for i in range(-3, 3)]

    templates += [(('pt', i), ('wl', i+1)) for i in range(-3, 3)]
 
    #'use' in the word
    #templates += [(('use', i), ('pos', i+1), ('pos', i+2)) for i in range(-3, 3)]


    disease_set = set()
    with open("gztr/disease.txt", "r") as f:
        for line in f:
            disease_set |= set(line.rstrip("\n").lower().split(" "))


    for seq, target_set in readiter(fi):
        for i, v in enumerate(seq):
            # Extract more characteristics of the input sequence
            v['iu'] = str(v['w'] and v['w'][0].isupper())
            v['wl'] = v['w'].lower()
            v['tr'] = str(v['w'] and v['w'] in target_set)
            v['di'] = str(v['w'] and v['w'] in disease_set)
            v['pt'] = str(v['w'] and bool(v['pos'] == 'TO'))
            v['use'] = str(v['w'] and 'use' in v['w'])
            #v['lm'] = lmtzr.lemmatize(v['w'])


        for t in range(len(seq)):
            fo.write(seq[t]['y'])
            for template in templates:
                attr = apply_template(seq, t, template)
                if attr is not None:
                    fo.write('\t%s' % escape(attr))
            fo.write('\n')
        fo.write('\n')

