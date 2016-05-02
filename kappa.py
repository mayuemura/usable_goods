#kappa.py
#-*- coding:utf-8 -*-
#2015/12/19
#2016/02/18 modified(rename)

import numpy as np
import sys

from pymongo import Connection


def kappa(nested_list):

    #[[],[],...[]]
    ag_total = 0.0
    total = nested_list[11,11]
    #total = nested_list[12,12]
    
    la_total = [nested_list[11, i] for i in range(11)]
    lb_total = [nested_list[i, 11] for i in range(11)]
    #la_total = [nested_list[12, i] for i in range(12)]
    #lb_total = [nested_list[i, 12] for i in range(12)]


    for i, line in enumerate(nested_list[:11]):
    #for i, line in enumerate(nested_list[:12]):
        ag_total += line[i]
    print ag_total

    po = ag_total/total
    pe = 0.0

    for i in range(11):
    #for i in range(12):
        pe += la_total[i]*lb_total[i]/(total*total)

    kappa = (po-pe)/(1-pe)

    return kappa

def confusion_matrix(arg):

    client = Connection("beer")
    db = client["usable_goods_SD"]
    collections = ["cosme", "health", "nlp2016"]

    """
    #cm = np.zeros((13,13))
    indx_dict = {
            "Target": 0,
            "Effect": 1,
            "NullEffect": 2,
            "DegreeOfEffect": 3,
            "CertaintyOfEffect": 4,
            "MeansOfUse": 5,
            "ComposedOf": 6,
            "PartOf": 7,
            "Location": 8,
            "Time": 9,
            "User": 10,
            "Version": 11
            }

    cm = np.zeros((12,12))
    indx_dict = {
            "Effect": 0,
            "NullEffect": 1,
            "DegreeOfEffect": 2,
            "CertaintyOfEffect": 3,
            "MeansOfUse": 4,
            "ComposedOf": 5,
            "PartOf": 6,
            "Location": 7,
            "Time": 8,
            "User": 9,
            "Version": 10
            }
    """


    if arg in collections:
        colls = [db[arg]]
    elif arg == "all":
        colls = [db[c] for c in collections]
    else:
        print "please input collection name or 'all'"

    for coll in colls:
        for document in coll.find({}):
            dp = document["dp_tag"]
            st = document["st_tag"]

            #if not (dp == "Target" or st == "Target"):
                #cm[11, 11] += 1
            #cm[12, 12] += 1
            if dp == None or st == None:
                continue
            else:
                try:
                    cm[indx_dict[dp], indx_dict[st]] += 1

                    cm[indx_dict[dp], 11] += 1
                    cm[11, indx_dict[st]] += 1
                    #cm[indx_dict[dp], 12] += 1
                    #cm[12, indx_dict[st]] += 1
                except KeyError:
                    if not (dp =="Target" or st == "Target"):
                        print dp, st
            
    la_total = [cm[11, i] for i in range(11)]
    lb_total = [cm[i, 11] for i in range(11)]
    #la_total = [cm[12, i] for i in range(12)]
    #lb_total = [cm[i, 12] for i in range(12)]
    la = sum(la_total)
    lb = sum(la_total)
    if la == lb:
        cm[-1,-1] = la
    else:
        print "total Error!"

    return kappa(cm)
    #return cm

if __name__ == "__main__":

    print confusion_matrix(sys.argv[1])
    #confusion_matrix(sys.argv[1])
#python kappa.py cosme
