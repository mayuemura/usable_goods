#FB_fetch_article.py
#-*- coding:utf-8 -*-
#2016/02/15

import glob
import os
import sys

def fetch_article(dirname):

    with open("data/{}/keyword.txt".format(dirname), "r") as f:
        for line in f:
            articleNo, Target = line.strip("\n").split("\t")
            target = Target.lower()
            #os.system("grep '^restores\t' Labels/Effect.txt > a.txt")
            os.system("grep -i '^{}	' facts.txt > Freebase/{}_{}.txt".format(Target, dirname, articleNo))
            #os.system("grep '^{}' facts.txt >> Freebase/{}_{}.txt".format(target, dirname, articleNo))

if __name__ == "__main__":
    fetch_article(sys.argv[1])

#python FB_fetch_article.py cosme --> fetch_article

"""
####API####

import json
import sys
import urllib
from rdflib import Graph
from rdflib.graph import ConjunctiveGraph

def main():
    api_key = open(".freebase_api_key").read()
    service_url = "https://www.googleapis.com/freebase/v1/rdf"
    topic_id = "/m/02h40lc"
    params = {
        "key": api_key
    }
    url = service_url + topic_id + "?" + urllib.urlencode(params)
    g = ConjunctiveGraph()
    g.load(url, format="n3")

    for s, p, o in g:
        print s, p, o

if __name__ == "__main__":
    main()
"""
