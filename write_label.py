#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' INPUT: the output of uniformize_distribution.py
Input should look like: VOA/bar/foo/file1.sdc [0.0,12.34]
This script creates all the files listed in the input within their directories
(created if missing) with new labels.
The files created contain the new label. See example below.
Example. VOA/bar/foo/file1.sdc --> creation of file1.lbl in folder VOA/bar/foo
file_lang1.lbl: "0.0 1.21 speech"

/!\/!\/!\/!\ Path are WINDOWS-LIKE. /!\/!\/!\/!\ 
'''

import os
import sys


def main(filename):
    ''' input: output of tri2.py (lang-uni.txt)
    output: create the directories and the label files''' 
    filename += '_uni.txt'
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        list_path = []
        list_lbl = []
        line_clean = line.rstrip('\n').strip().split(' ')
        filename = line_clean[0]
        list_lbl_tmp = line_clean[1:]
        list_lbl = [float(list_lbl_tmp[0][1]), float(list_lbl_tmp[1][:-1])]
        list_path = filename.split('/')
        for i in range(len(list_path)):
            if i == 0:
                pass
            else:
                list_path[i] = list_path[i-1] + '\\' + list_path[i]
        for path in list_path[:-1]:
            try:
                os.mkdir(path)
            except OSError:
                pass
        list_path[-1] = list_path[-1].rstrip('sdc')
        list_path[-1] = list_path[-1] + 'lbl'
        file_line = open(list_path[-1], 'w')
        file_line.write(str(list_lbl[0]) + ' ' + str(list_lbl[1]) + ' speech')
        file_line.close()


target_lang  = ['alev', 'amag', 'amer', 'amha', 'amsa', 'beng', 'bosn', 'cant',\
               'creo', 'croa', 'czec', 'dari', 'fren', 'geor', 'haus', 'hind',\
               'indi', 'iraq', 'kore', 'laot', 'mand', 'pash', 'pers', 'poli',\
               'port', 'punj', 'russ', 'slov', 'span', 'tami', 'thai', 'turk',\
               'ukra', 'urdu', 'viet']

for lang in target_lang:
    main(lang)
