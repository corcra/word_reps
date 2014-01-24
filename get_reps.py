#!/usr/bin/python
# author:       Stephanie Hyland sh985@cornell.edu
# date:         January 2014
# description:  This script takes a pickled list of words in varying states of disrepair (_master_dictionary.pk), strips (),[],start/end underscores, splits x/y into x and y, and removes fully numeric words.
#               It then compares with a list of word representations (google_words.txt.gz - derived from the Google word list), to get representations for words in the pickled list. (written to master_reps.txt)
#               The unmatched words are written to unmatched.txt.
# usage:        python get_reps.py google_word_path master_dict_path
# output:       in the same folder, master_reps.txt and unmatched.txt
#
import numpy as np
import re
import gzip
import sys

def cleanup(s):
    s_clean = re.sub('(\x00|\n)','',s)
    return s_clean

google_word_path = sys.argv[1]
master_dict_path = sys.argv[2]

master = np.load(master_dict_path)

filtered = []
# get rid of brackets (anywhere) and underscores from start/end
# split on a slash and make into two words

for w in master:
    w_strip = re.sub('(^_|_$)|[()\[\]]','',w)
    if len(w_strip)>1:
        w_split = w_strip.split('/')
        for w_bit in w_split:
            # exclude entries which are ALL numerical
            try:
                w_bit = float(w_bit)
                continue
            except ValueError:
                filtered.append(w_bit)

print 'Preprocessing complete.'
#np.savetxt("filtered_dictionary.txt",filtered,fmt="%s")

msk_set = set(filtered)
n_total = len(msk_set)
print 'There are',n_total,'unique "words" in the set.'

# now overlaps with the vector reps (google words)
gw = gzip.open(google_word_path,'r')
line_total = 3000000

# outfile
outfilename = 'master_reps.txt'
outfile = open(outfilename,'w')

print 'Looking for vector representations in '+repfilename
l = 0
n = 0
for line in gw:
    perc = 100.0*l/line_total
    if perc%10==0:
        sys.stdout.write('\r'+str(perc)+'%')
        sys.stdout.flush()
    l = l+1

    splitline = line.split()
    word = cleanup(splitline[0])
    if word in msk_set:
        splitline[0] = word
        newline = ' '.join(splitline)
        outfile.write(newline+'\n')
        n = n +1
        msk_set.remove(word)

print '\nVector representations for '+str(n)+' ('+str(100*float(n)/n_total)+'%) words recorded to',outfilename

unmatchfile = open('unmatched.txt','w')
unmatchfile.write(str(len(msk_set))+' unmatched words:\n')
for word in msk_set:
    unmatchfile.write(word+'\n')
