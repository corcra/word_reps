word_reps
=========

Scripts pertaining to processing/clustering vector representations of words.

Roughly this corresponds to a pipeline:  
- Get a binary file of vector reps for 3m words (https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM).   
  These representations were obtained after training on part of a Google News database (~100b words) using word2vec (https://code.google.com/p/word2vec/).  
- Convert this to plaintext using bin_to_plain.c  
This is a modified version of word2vec's distance.c, because I couldn't figure out how else to decode the binary file.   
Note: need/want to gzip the result of this.  
- Using a .pk list of desired words, get representations for these (get_rep.py).  
Essentially search in the reference Google file, with some processing.  
- Do kmeans clustering on the result (get_clusters.py).  
Investigating alternate clustering methods currently.  
- Analyse the cluster results (analyse_clusters.r).  
Assume 'best' clusters have lowest mean distance-to-centroid, hope these correspond to semantically similar words.  
  
There's also a script (get_wordcloud.py) which will create a wordcloud from a cluster, but this has several dependencies.
