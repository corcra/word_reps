#!/usr/bin/python
# author:       Stephanie Hyland (sh985@cornell.edu)
# date:         January 2014
# description:  The purpose of this script is to take an input dataset and cluster it somehow.
#
# Implemented approaches:
# 1. k-means, using scipy.cluster.vq.kmeans.
#
# Other approaches to consider (thanks Theo!):
# 1. n nearest-neighbour
# 2. epsilon-ball
# 
# Possibly not a real approach:
# 1. try to fit a concentration graph (metric to use? partial correlation may not capture the correct notion of distance, but then you lose the theory behind the graph - requires further consideration), then look for connected clusters
#
# usage:        python get_clusters.py word_vecs.txt
# note:         word_vecs.txt should consist of only vector components (floats). The script looks for the corresponding words in the file word_vecs.words.txt. Given the my_reps.txt (output of get_reps.py) this is simple:
#               cut -d ' ' -f 2- my_reps.txt > word_vecs.txt
#               awk '{ print $1 }' my_reps.txt > word_vecs.words.txt
#
# output:       word_vecs.clusters.txt, consisting of word, cluster assignment, distance to cluster centroid

import sys
import numpy as np
from scipy.cluster.vq import whiten
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import vq

if len(sys.argv)<3:
    print "Usage: python get_clusters.py word_vecs.txt N_CLUST"
    print "Perhaps necessary:\n\tcut -d ' ' -f 2- my_reps.txt > word_vecs.txt\n\tawk '{ print $1 }' my_reps.txt > word_vecs.words.txt"
    sys.exit()

N_CLUST = int(sys.argv[2])

# filenames
datafile_name = sys.argv[1]
wordlist_name = datafile_name.replace('.txt','.words.txt')
clusterlist_name = datafile_name.replace('.txt','.clusters.'+str(N_CLUST)+'.txt')

# data
data = np.loadtxt(datafile_name)
# normalise the data ('whiten')
white_data = whiten(data)
words_mess = open(wordlist_name,'r').readlines()
words = np.array(map(str.strip,words_mess))
print 'Data acquired!'

# outfile
cluster_file = open(clusterlist_name,'w')

# kmeans clusering
print 'Clustering!'
clust = kmeans(white_data,N_CLUST)
clust_codebook = clust[0]

print 'Cluster centroids obtained, making assignments...'
vq_out = vq(white_data,clust_codebook)
kmeans_assignments = vq_out[0]
distances = vq_out[1]

for i in range(len(words)):
    word = words[i]
    cluster_assignment = kmeans_assignments[i]
    dist_to_centroid = distances[i]
    cluster_file.write(str(word)+'\t'+str(cluster_assignment)+'\t'+str(dist_to_centroid)+'\n')

mean_distance = np.mean(distances)
print 'Mean distance to centroid:',mean_distance
