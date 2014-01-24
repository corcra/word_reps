#!/usr/bin/python
# author:       Stephanie Hyland (sh985@cornell.edu)
# date:         January 2014
# description:  create a word cloud from a list of words (weighted using distance to centroid). Uses 'wordcloud' (http://peekaboo-vision.blogspot.de/2012/11/a-wordcloud-in-python.html).
# usage:        python get_wordcloud.py wordlist.txt number 
#               The wordlist should be columns of word - cluster assignment - distance to centroid (output of get_clusters.py). number is just the number of the cluster of interest.
# output:       wordlist_name.png - a wordcloud..
#
import sys
import numpy as np
sys.path.insert(0, './word_cloud-master/')
import wordcloud

if len(sys.argv)<3:
    sys.exit("Usage: python get_wordcloud.py wordlist.txt number")

wordlist_name = sys.argv[1]
cluster_number = sys.argv[2]
wordlist_file = open(wordlist_name,'r')

words = []
dists = []
# the distances are to the centroid
for line in wordlist_file:
    word = line.split()[0]
    cluster = line.split()[1]
    dist = float(line.split()[2])
    if cluster==cluster_number:
        words.append(word)
        dists.append(dist)

max_dist = max(dists)*1.05
weights = [max_dist - dist for dist in dists]

words_array = np.array(words)
weights_array = np.array(weights)

wordcloud.make_wordcloud(words_array,weights_array,wordlist_name+'.'+cluster_number+'.png')
