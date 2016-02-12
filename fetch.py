#fetch.py
#-*- coding:utf-8 -*-
#2015/10/30
#2015/12/22 modified
#2016/02/12 modified INPUT:word --> INPUT:keyword file

import json
import os.path
import re
import sys
import urllib


del_ptrn1 = re.compile("r\{\{Infobox.+?\}\}|\{\{|\}\}|\[\[|\]\]|''+|[Ff]ile\:.*?\n|[Ii]mage\:.*?\n", re.DOTALL)
del_ptrn2 = re.compile(r"<ref name=\w*/>|<ref.*?>.*?</ref>|<div class=.*?>", re.DOTALL)
replace_ptrn1 = re.compile(r"<([a-z]+?)>(.*?)</\1>", re.DOTALL)
replace_ptrn2 = re.compile(r"[(A-Z][a-z)]+.?\|([a-zA-Z]+?)", re.DOTALL)

redirect_ptrn = re.compile(r"\#REDIRECT\s*\[\[([a-zA-Z0-9#\s\(\)]*?)\]\].*")

def redirect(revisions):
    try:
        new_title = redirect_ptrn.match(revisions).group(1)
        fetch_word(new_title.split("#")[0])
    except AttributeError:
        print revisions


def json_gomitori(word, data_json):

    try:
        content = data_json["query"]["pages"].values()[0]
        revisions = content["revisions"][0].get("*", None)
        title = content["title"].replace(" ", "_")

        if revisions == None:
            print word + ": not exist"

        elif revisions.startswith("#REDIRECT"):
            redirect(revisions)
        
        else:
            gomitori1 = del_ptrn1.sub("", revisions)
            gomitori2 = del_ptrn2.sub("", gomitori1)
            okikae1 = replace_ptrn1.sub(r"\2", gomitori2)
            okikae2 = replace_ptrn2.sub(r"\1", okikae1)

            with open("wiki/"+title.replace("/", "_")+".txt", "w") as fo:
                for line in okikae2.split("\n"):
                    if line.startswith("=="):
                        break
                    else:
                        fo.write(line)

            with open("keywords.txt", "a") as f:
                f.write(title+"\n")
    
    
    except KeyError:
        print word + ": not exist"

def fetch_word(keyword):
    url = "http://en.wikipedia.org/w/api.php?"
    params = urllib.urlencode({
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "rvprop": "content",
	    "titles": keyword
    })
    data = urllib.urlopen(url + params).read()

    json_gomitori(keyword, json.loads(data))



def fetch_file(keyword_file):

    with open(keyword_file, "r") as f:
        for line in f:
            keyword = line.rstrip("\n")

            url = "http://en.wikipedia.org/w/api.php?"
            params = urllib.urlencode({
                    "action": "query",
                    "format": "json",
                    "prop": "revisions",
                    "rvprop": "content",
	            "titles": keyword
            })
            data = urllib.urlopen(url + params).read()

            json_gomitori(keyword, json.loads(data))


if __name__ == "__main__":
    INPUT = sys.argv[1]
    if INPUT.endswith(".txt"):
        fetch_file(INPUT)
    else:
        fetch_word(INPUT)

#python fetch.py deepika_keywords.txt
