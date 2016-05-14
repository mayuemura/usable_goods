#!/home/may-u/may/bin/python2.7
#-*- coding:utf-8 -*-
#xml_brat.py
#2016/05/05


import glob
import itertools
import sys
import xmltodict

from collections import OrderedDict

def make_CRFdata(domain):
    xml_files = sorted(glob.glob("stanford/xml_out/{}/*.out".format(domain)))
    ann_files = sorted(glob.glob("data/{}/deepika/*.ann".format(domain)))


    TAGs = {
            "Target": "Trg",
            "Effect": "Eff",
            "NullEffect": "Null",
            "DegreeOfEffect": "Deg",
            "CertaintyOfEffect": "Cer",
            "ComposedOf": "Com",
            "Location": "Loc",
            "Time": "Time",
            "User": "User",
            "Version": "Ver",
            "MeansOfUse": "MOU",
            "PartOf": "Part"
            }


    for xml, ann in itertools.izip(xml_files, ann_files):
        xml_No = xml.split("/")[-1].split("_")[0]
        ann_No = ann.split("/")[-1].split("_")[0]
        indx = 0

        if not xml_No == ann_No:
            print "file number error\n"
        else:
            with open(ann, "r") as A:

                #ファイル内のアノテーションをすべてann_listに格納
                ann_list = list()
                xml_list = list()
                for line in A:
                    if line.startswith("R") or line.startswith("#"):
                        continue
                    else:
                        try:
                            l = line.split()
                            ann_dict = {
                                "segmentNo": l[0],
                                "tag": l[1],
                                "Begin": int(l[2]),
                                "End": int(l[3]),
                                "words": " ".join(l[4:])
                            }
                        except ValueError:
                            pass
                            #print "value error happened in this file: " + ann


                    ann_list.append(ann_dict)
                ann_list.sort(key=lambda x: int(x["Begin"]))


                X = xmltodict.parse(open(xml))
                sentence = X['root']['document']['sentences']['sentence']

                # たまにsentenceのtypeがlistじゃないときがあるので（health）
                if not isinstance(sentence, list):
                    sentence = [sentence] 


                for indx, tokens in enumerate(sentence):

                    for token in tokens['tokens']['token']:
                        xml_list.append({
                            "word": token['word'],
                            "Begin": int(token['CharacterOffsetBegin']),
                            "End": int(token['CharacterOffsetEnd']),
                            "POS": token['POS'],
                            "NER": token['NER'],
                            "tag": ""
                            })
                    xml_list.append("EOS")

            # Targetとなる単語（記事タイトル）を最初に表示
            title = ann.split("/")[-1].split(".")[0].lstrip(ann_No+"_").replace("_", " ")
            yield "#\t{},{}".format(title, title.lower())

            for xml in xml_list:

                if xml == "EOS":
                    yield ""
                else:
                    # ann_listにBIO適応していないアノテーションがあれば
                    if ann_list:

                        ann = ann_list[0]

                        B_xml = xml['Begin']
                        E_xml = xml['End']
                        B_ann = ann['Begin']
                        E_ann = ann['End']


                        # segmentの長さが1単語
                        if B_xml == B_ann and E_xml == E_ann:
                            xml['tag'] = "B-" + TAGs[ann['tag']]
                            ann_list.pop(0)

                        # 見ている単語が2語以上のsegmentの先頭
                        elif B_xml == B_ann and E_xml != E_ann:
                            xml['tag'] = "B-" + TAGs[ann['tag']]

                        # 見ている単語が2語以上のsegmentの最後
                        elif E_xml == E_ann and B_xml != B_ann:
                            xml['tag'] = "I-" + TAGs[ann['tag']]
                            ann_list.pop(0)

                        # segmentの中
                        elif E_xml < E_ann and B_xml > B_ann:
                            xml['tag'] = "I-" + TAGs[ann['tag']]

                        # それ以外
                        else:
                            xml['tag'] = "O"

                    # ann_listの中身がないとき（アノテーション終了）
                    else:
                        xml['tag'] = "O"

                # ファイルを指定して確認
                #if xml_No == "23":
                #    for xml in xml_list:
                #        print xml

                    yield "{}\t{}\t{}\t{}".format(xml['tag'], xml['word'], xml['POS'], xml['NER'])

if __name__ == "__main__":
    INPUT = sys.argv[1]
    domains = {"cosme", "health", "nlp2016", "pricai2016"}

    # ドメイン指定してそれぞれ作る
    if INPUT in domains:
        for result in make_CRFdata(INPUT):
            print result

    # 全部まとめて作る
    elif INPUT == "all":
        for domain in domains:
            for result in make_CRFdata(domain):
                print result



#python xml_brat.py
