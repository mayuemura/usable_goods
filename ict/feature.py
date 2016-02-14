#!/usr/bin/env python

import sys

def readiter(fi, names=('y', 'w', 'pos'), sep='\t'):
    seq = []
    for line in fi:
        line = line.strip('\n')
        if not line:
            yield seq
            seq = []
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

    templates = []
    templates += [(('w', i),) for i in range(-3, 4)]
    templates += [(('w', i), ('w', i+1)) for i in range(-3, 3)]
    templates += [(('pos', i),) for i in range(-3, 4)]
    templates += [(('pos', i), ('pos', i+1)) for i in range(-3, 3)]
    #templates += [(('chk', i),) for i in range(-2, 3)]
    #templates += [(('chk', i), ('chk', i+1)) for i in range(-2, 2)]
    templates += [(('iu', i),) for i in range(-3, 4)]
    templates += [(('iu', i), ('iu', i+1)) for i in range(-3, 3)]

    #EffectModifier
    templates += [(('em', i),) for i in range(-3, 4)]
    templates += [(('em', i), ('em', i+1)) for i in range(-3, 3)]
    #ComposedOf
    templates += [(('com', i),) for i in range(-3, 4)]
    templates += [(('com', i), ('com', i+1)) for i in range(-3, 3)]
    #PartOf
    templates += [(('part', i),) for i in range(-3, 4)]
    templates += [(('part', i), ('part', i+1)) for i in range(-3, 3)]
    #Location
    templates += [(('loc', i),) for i in range(-3, 4)]
    templates += [(('loc', i), ('loc', i+1)) for i in range(-3, 3)]
    #Time
    templates += [(('time', i),) for i in range(-3, 4)]
    templates += [(('time', i), ('time', i+1)) for i in range(-3, 3)]
    #User
    templates += [(('user', i),) for i in range(-3, 4)]
    templates += [(('user', i), ('user', i+1)) for i in range(-3, 3)]
    #Version
    templates += [(('ver', i),) for i in range(-3, 4)]
    templates += [(('ver', i), ('ver', i+1)) for i in range(-3, 3)]
    #Target
    templates += [(('tar', i),) for i in range(-3, 4)]
    templates += [(('tar', i), ('tar', i+1)) for i in range(-3, 3)]




    file_list = [
            "gztr/EffectModifier.txt",
            "gztr/ComposedOf_gztr.txt",
            "gztr/PartOf_gztr.txt",
            "gztr/Location_gztr.txt",
            "gztr/Time_gztr.txt",
            "gztr/User_gztr.txt",
            "gztr/Version_gztr.txt",
            "gztr/Target_gztr.txt"
            ]
    dict_list = list()

    for gazetteer in file_list:
        with open(gazetteer, "r") as f:
            d = dict()
            for line in f:
                words = line.rstrip("\n").split(" ")
                d[words[0]] = "B"
                for word in words[1:]:
                    d[word] = "I"
            dict_list.append(d)

    EffectModifier = dict_list[0]
    ComposedOf = dict_list[1]
    PartOf = dict_list[2]
    Location = dict_list[3]
    Time = dict_list[4]
    User = dict_list[5]
    Version = dict_list[6]
    Target = dict_list[7]

    for seq in readiter(fi):
        for v in seq:
            # Extract more characteristics of the input sequence
            v['iu'] = str(v['w'] and v['w'][0].isupper())

            v['em'] = str(v['w'] and EffectModifier.get(v['w'], "O"))
            v['com'] = str(v['w'] and ComposedOf.get(v['w'], "O"))
            v['part'] = str(v['w'] and PartOf.get(v['w'], "O"))
            v['loc'] = str(v['w'] and Location.get(v['w'], "O"))
            v['time'] = str(v['w'] and Time.get(v['w'], "O"))
            v['user'] = str(v['w'] and User.get(v['w'], "O"))
            v['ver'] = str(v['w'] and Version.get(v['w'], "O"))
            v['tar'] = str(v['w'] and Target.get(v['w'], "O"))


        for t in range(len(seq)):
            fo.write(seq[t]['y'])
            for template in templates:
                attr = apply_template(seq, t, template)
                if attr is not None:
                    fo.write('\t%s' % escape(attr))
            fo.write('\n')
        fo.write('\n')
