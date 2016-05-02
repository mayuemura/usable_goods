#FB_relation_grep.py
#-*- coding:utf-8 -*-
#2016/02/16

import sys
#from pymongo import Connection

def relation_grep(FB_files):

    #client = Connection("beer")
    #db = client["usable_goods"]
    #coll = db[FB_files[0].split("/")[1].split("_")[0]]


    with open("Freebase/except_relation", "r") as fr, open("Freebase/except_value", "r") as fv:
        except_relation = set(fr.read().split("\n"))
        except_value = set(fv.read().split("\n"))
    
    total_rel_dic = dict()
    example_dic = dict()
    with open("Freebase/relation_pattern", "r") as f:
        #relation_pattern = set(f.read().split("\n"))
        for line in f:
            relation = line.rstrip("\n")
            total_rel_dic[relation] = 0
            example_dic[relation] = set()

    for FB_file in FB_files:
        articleNo = FB_file.split("_")[1].rstrip(".txt")
        value_set = set()
        doc_set = set()

        with open(FB_file, "r") as f:
            for line in f:
                entity, relation, value = line.rstrip("\t.\n").split("\t")
                if relation in except_relation or value in except_value:
                    continue
                elif relation in example_dic.keys():
                    value_set.add(value)
                    example_dic[relation].add(value)

            print FB_file
            for k, v in example_dic.iteritems():
                if len(v) == 0:
                    continue
                else:
                    print "{}\t{}\t{}".format(k, len(v), ", ".join(v))

                total_rel_dic[k] += len(v)
                example_dic[k] = set()

            print "\n"
    print total_rel_dic

        #for doc in coll.find({"articleNo":articleNo, "annotator":"st", "$or":[{"st_tag":"Effect"}, {"st_tag":"MeansOfUse"}]}):
        #    doc_set.add(doc["words"])
        
        #print FB_file
        #print "FB", value_set
        #print "rel", rel_dic
        #print "Wiki", doc_set
        #print "\n"


        #for value in value_set:
        #    for doc in doc_set:
        #        if value in doc:
        #            print value, doc
                

if __name__ == "__main__":
    relation_grep(sys.argv[1:])

#python FB_relation_grep.py [FB_file]
