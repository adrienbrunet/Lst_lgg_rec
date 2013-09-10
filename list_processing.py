#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Dealing with list processing for language recognition: 
- uniform distribution and label manipulation
- PLDA list

---- Uniform distribution and label change
From a list of audio samples, generate an other list with labels so the
considered list is then uniformly distribute. In main, you can change the Number
of Interval you want your distribution to fit in. 

Optional: see main and uncomment lines if needed
- Plot the distribution of the length duration for the language before 
and after uniformization
- Plot duration accumulation

INPUT: a file (or several files listed in target_lang) with a list of lines :
"filename duration [label]"
Those filenames are from ONE language only.

OUTPUT: see write_output to change the output filename.
The output is a list where labels has been added. (filename duration [label])
Further processing could be needed, see write_label.py

---- PLDA List
INPUT: a file (or several files listed in target_lang) with a list of lines :
"filename duration [label]" duration and label could be omitted 
Those filenames are from ONE language only.

OUTPUT: a list which suits PLDA needs: 50 files per line
exemple: file1 file2 file3 file4 ... file50
         File1 File2 File3 File4 ... File50
'''

from collections import deque
from random import randint
import matplotlib.pyplot as plt

target_lang = ['alev', 'amag', 'amer', 'amha', 'amsa', 'beng', 'bosn', 'cant',\
               'creo', 'croa', 'czec', 'dari', 'fren', 'geor', 'haus', 'hind',\
               'indi', 'iraq', 'kore', 'laot', 'mand', 'pash', 'pers', 'poli',\
               'port', 'punj', 'russ', 'slov', 'span', 'tami', 'thai', 'turk',\
               'ukra', 'urdu', 'viet']


class Lst(object):

    def __init__(self, filename):
        self.filename = filename
        self.rows          = self.load_lst()
        self.nb_file_global, self.max_duration_global = self.process_row(self.rows)
        self.old_list = []
        self.new_list = []
        self.sorted_list = []
        self.sorted_list_imm = []
        for rr in self.rows:
            self.old_list.append(File(rr))
        self.sorted_list = list(self.old_list)
        self.sorted_list.sort()
        self.sorted_list_imm = self.sorted_list
        self.sorted_list = deque(self.sorted_list)

    def load_lst(self):
        ''' Load filename which should look like: "filename duration [label]"
        Exemple file: list.txt
        >>> List = Lst('list.txt')
        '''
        list = open(self.filename, "r")
        rows = list.readlines()
        list.close()
        return rows

    def process_row(self, rows):
        ''' We gather basic informations on the current list:
            begin, nb_file_global, max_duration_global
        >>> List = Lst('list.txt')
        >>> print List.nb_file_global, List.max_duration_global
        3 1000
        '''
        nb_file_global      = len(rows)
        max_duration_global = max(list(int(row.split(" ")[1]) for row in rows))
        return nb_file_global, max_duration_global

    def uniformize(self, nb_int):
        ''' distribute 1 file per interval with nb_int interval, changing label
        if needed, then redistribute the rest to uniformize the distribution'''
        nb_int = int(nb_int)
        for foo in range(nb_int-1):
            self.new_list.append(Interval(foo, foo + 1))
        while self.sorted_list != deque([]):
            self.redistribute(nb_int)


    def change_label(self, interval, listfile):
        '''Change the label so the length of the file correspond to
        the interval.'''
        label_max = interval.max
        label_min = interval.min
        new_time = randint(label_min * 100, label_max * 100)
        if new_time == 0:
            new_time = 1
        new_time = new_time / 100.0
        listfile[0].label.extend([0, new_time])

    def redistribute(self, nb_previous_interval):
        ''' When intervalls are full and you still have a lot of files with
        smaller duration than the next intervals duration, it redistributes
        those files to the pre-existent (and full) intervals.
        '''
        target_interval_1 = min(self.new_list[0:nb_previous_interval-1])
        time_limit = int(self.sorted_list[0].duration / 100.0)
        target_interval_2 = min(self.new_list[0:time_limit - 1])
        minimum = min(target_interval_1.min, target_interval_2.min)
        target_interval = self.new_list[minimum]
        self.change_label(target_interval, self.sorted_list)
        self.new_list[target_interval.min].list_files.append(self.sorted_list.popleft())

    def plot_duration_old(self):
        ''' Plot the accumulation of file duration'''
        A = []
        A = self.sorted_list_imm
        len_a, max_a = len(A), (max(A).duration)/100 + 1
        count_list = []
        for ii in range(max_a):# 1s interval from 0 to max_a
            ccount = 0
            jj = 0
            while (A[jj].duration / 100.0) < float(ii):
                ccount += 1
                jj += 1
                if jj == len_a:
                    break
            count_list.append(len_a - ccount)
        plt.figure()
        plt.plot(count_list)
        plt.title("Accumulation | Duration - " + lang)
        plt.ylabel("Numbers of files longer than x")
        plt.xlabel("File's length in secondes")
        plt.show()

    def write_output(self, lang):
        ''' Write in lang-uni.txt the files with the new labels '''
        fn = lang + '_uni.txt'
        file1 = open(fn, "w")        
        for llist in self.new_list:
            for el in llist.list_files:
                file1.write(str(el.filename) + ' ' + str(el.label) + '\n')

    def plot_new_and_old_distrib(self):
        '''2 lists with the duration in second'''
        L_old, L_new = [], []
        for llist_int in self.new_list:
            for el in llist_int.list_files:
                L_old.append(float(el.duration)/100)
                if el.label == []:
                    L_new.append(float(el.duration)/100)
                else:
                    L_new.append(float(el.label[-1]))
        plt.figure()
        plt.hist(L_old, 50)
        plt.title("Files' length distribution before uniformization - " + lang)
        plt.xlabel("Duration in seconds")
        plt.ylabel("Number of files")
        plt.show()
        plt.figure()
        plt.hist(L_new, 50)
        plt.title("Files' length distribution after uniformization - " + lang)
        plt.xlabel("Duration in seconds")
        plt.ylabel("Number of files")
        plt.show()

    def build_plda_list(self, lang):
        ''' Write a PLDA_list in lang-plda.txt'''
        fn = lang + '_plda.txt'
        file1 = open(fn, "w") 
        while len(self.rows) != 0:
            line = []
            while len(line) < 50:
                if len(self.rows) == 0: break
                else: line.append(self.rows.pop())
            s = ""
            for name in line:
                s += name.rstrip().split()[0]
                s += " "
            file1.write(s + "\n")



class File(object):
    ''' From a string "filename duration...", creates an object
    with the corresponding attributes'''

    def __init__(self, string):
        string = string.rstrip('\n').strip().split(' ')
        if len(string) < 2:
            print 'Not enough input argument to create this file object'
        else:
            self.filename = string[0]
            self.duration = int(string[1])
            self.label    = list(int(el) for el in string[2:])

    def __str__(self):
        return self.filename

    def __repr__(self):
        return self.filename + ' ' + str(self.duration)

    def __cmp__(self, other):
        return cmp(self.duration, other.duration)


class Interval(object):
    '''Define an Interval, with a list, a maximum and a minimum length.'''

    def __init__(self, begin, end):
        self.list_files = []
        self.min = begin
        self.max = end

    def __str__(self):
        s = ''
        for el in self.list_files:
            s += str(el.filenames)
        return s

    def __repr__(self):
        return 'nb_files: ' + str(len(self.list_files)) + ' | interval: [' +\
        str(self.min) +  ', ' + str(self.max) + '] \n'

    def __cmp__(self, other):
        return cmp(len(self.list_files), len(other.list_files))


def main(lang):
    '''To run'''
    filename = lang + '-frame.lst' # To fit the names of your lists
    List = Lst(filename)
    #### UNIFORMIZATION
    #---------------------------------------------------------------------------
    #List.uniformize(31) # You can modify this number
    #List.plot_new_and_old_distrib()
    #List.plot_duration_old()
    #List.write_output(lang)

    #### PLDA List building
    #---------------------------------------------------------------------------
    List.build_plda_list(lang)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


# ACTUALLY RUN YOUR SCRIPT
for lang in target_lang:
    main(lang)
