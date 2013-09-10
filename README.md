Lst_lgg_rec
===========

see list_processing.py and write_label.py

Dealing with list processing for language recognition: 
- uniform distribution and label manipulation
- PLDA list

Uniform distribution and label change
--------------------------------------

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

PLDA List
---------

INPUT: a file (or several files listed in target_lang) with a list of lines :
"filename duration [label]" duration and label could be omitted 
Those filenames are from ONE language only.

OUTPUT: a list which suits PLDA needs: 50 files per line
exemple: file1 file2 file3 file4 ... file50
         File1 File2 File3 File4 ... File50
