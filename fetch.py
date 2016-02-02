#fetch.py
#-*- coding:utf-8 -*-
#2015/10/30
#2015/12/22 modified

import json
import os.path
import re
import sys
import urllib


del_ptrn1 = re.compile("r\{\{Infobox.+?\}\}|\{\{|\}\}|\[\[|\]\]|''+|[Ff]ile\:.*?\n|[Ii]mage\:.*?\n", re.DOTALL)
del_ptrn2 = re.compile(r"<ref name=\w*/>|<ref.*?>.*?</ref>|<div class=.*?>", re.DOTALL)
replace_ptrn1 = re.compile(r"<([a-z]+?)>(.*?)</\1>", re.DOTALL)
replace_ptrn2 = re.compile(r"[(A-Z][a-z)]+.?\|([a-zA-Z]+?)", re.DOTALL)


def redirect(revisions):
    new_title = revisions.lstrip("#REDIRECT [[").rstrip("]]")
    fetch(new_title)


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



def fetch(keyword):

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
    fetch(sys.argv[1])
