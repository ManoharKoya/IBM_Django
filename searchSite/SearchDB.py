#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import nltk
import sqlite3
import csv
from queryInfo import QueryInfo
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


ps = PorterStemmer()
StopWds = set(stopwords.words("english"))



def MyFormula(na, nt, c1, c2, ct1, ct2):
    if na/nt > 1:
        konst = (float)(nt/na)
    else:
        konst = (float)(na/nt)
    res = 0.25*konst + 0.75*(float)(((float)(ct1/c1)+(float)(ct2/c2))/2)
    return res


def retTags(Title):
    A = -1
    words = nltk.word_tokenize(Title)    # words should be proper nouns
    taggedP = nltk.pos_tag(words)
    Realtags = []
    for (a, b) in taggedP:
        if(b == 'NNP' or b == "NN"):
            Realtags.append(a)
            A = 0
    rtags = [ps.stem(w) for w in Realtags]
    return rtags


def fun(text):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("""
            select * from infoData
            """)
    f = c.fetchall()
    tags = retTags(txt)
    conn.close()
    Alist = []

    for (a, b, c, d, e) in f:
        obj = QueryInfo(a, b, c, d)
        for i in tags:
            if i in e:
                Alist.append((a, b, c, d))
                break

    Aset = {('hello man', 0.0)}

    for (a, b, c, d) in Alist:
        ct1 = 0
        ct2 = 0
        c2 = 0
        c1 = 0
        W = nltk.word_tokenize(a)
        k11 = [ps.stem(w) for w in W]
        k1 = [w for w in k11 if w not in StopWds]
        W = nltk.word_tokenize(txt)
        k22 = [ps.stem(w) for w in W]
        k2 = [w for w in k22 if w not in StopWds]

        na = len(k11)
        nt = len(k22)
        for w in k1:
            if w in k2:
                ct1 += 1
            c1 += 1
        for w in k2:
            if w in k1:
                ct2 += 1
            c2 += 1
        f = MyFormula(na, nt, c1, c2, ct1, ct2)
        Aset.add((a, f))

    return Aset
            
