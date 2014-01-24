#!/usr/bin/python
# author:       Stephanie Hyland sh985@cornell.edu
# date:         January 2014
# description:  This script takes a pickled list of words in varying states of disrepair (_master_dictionary.pk), strips (),[],start/end underscores, splits x/y into x and y, and removes fully numeric words.
#               It then compares with a list of word representations (google_words.txt.gz - derived from the Google word list), to get representations for words in the pickled list. (written to my_reps.txt)
#               The unmatched words are written to unmatched.txt.
# usage:        python get_reps.py google_word_path my_dict_path
# output:       in the same folder, my_reps.txt and unmatched.txt
#
import numpy as np
import re
import gzip
import sys

def cleanup_google(s):
    s_stripped = re.sub('(\x00|\n)','',s)
    s_lower = s_stripped.lower()
    return s_lower

def cleanup_mine(s):
    s_stripped = re.sub('(^_|_$)|[()\[\]]','',w)
    s_lower = s_stripped.lower()
    return s_lower

if len(sys.argv)<3:
    sys.exit("Usage: python get_reps.py refs mine")

google_word_path = sys.argv[1]
if not '.gz' in google_word_path:
    sys.exit("Reference must be gzipped.")
my_dict_path = sys.argv[2]
if not '.pk' in my_dict_path:
    sys.exit("Wordlist must be pickled.")

mine = np.load(my_dict_path)
print "Words loaded from ",my_dict_path

filtered = []
# get rid of brackets (anywhere) and underscores from start/end
# split on a slash and make into two words
# make lowercase 

for w in mine:
    w_clean = cleanup_mine(w)
    if len(w_clean)>1:
        w_split = w_clean.split('/')
        for w_bit in w_split:
            # exclude entries which are ALL numerical
            try:
                w_bit = float(w_bit)
                continue
            except ValueError:
                filtered.append(w_bit)

print 'Preprocessing complete.'
#np.savetxt("filtered_dictionary.txt",filtered,fmt="%s")

my_set = set(filtered)
n_total = len(my_set)
print 'There are',n_total,'unique "words" in the set.'

# now overlaps with the vector reps (google words)
gw = gzip.open(google_word_path,'r')
line_total = 3000000

# outfile
outfilename = 'my_reps.txt'
outfile = open(outfilename,'w')

print 'Looking for vector representations in '+google_word_path
l = 0
n = 0
for line in gw:
    perc = 100.0*l/line_total
    if perc%10==0:
        sys.stdout.write('\r'+str(perc)+'%')
        sys.stdout.flush()
    l = l+1

    splitline = line.split()
    word = cleanup_google(splitline[0])
    if word in my_set:
        splitline[0] = word
        newline = ' '.join(splitline)
        outfile.write(newline+'\n')
        n = n +1
        my_set.remove(word)

print '\nVector representations for '+str(n)+' ('+str(100*float(n)/n_total)+'%) words recorded to',outfilename

unmatchfile = open('unmatched.txt','w')
unmatchfile.write(str(len(my_set))+' unmatched words:\n')
for word in my_set:
    unmatchfile.write(word+'\n')
