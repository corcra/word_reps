# author:       Stephanie Hyland (sh985@cornell.edu)
# date:         January 2014
# description:  script to analyse clusters manually. Find mean distance to centroid in each cluster, take top 10 clusters by this metric, see members
# usage:        source('analyse_clusters.r') in R

#args<-commandArgs(TRUE)
#filepath<-args[1]

print(list.files())
filepath<-readline("File? ")
#filepath = 'm_vecs.clusters.95.txt'

cwords<-function(data,c){
    clust<-da[da$"clust"==c,]
    print(clust$"word")
    browser()
}

da<-read.table(filepath,as.is=TRUE)
names(da)<-c("word","clust","dist")

n_clust<-range(da$"clust")[2]
clust_means<-rep(0,n_clust)
clust_sd<-rep(0,n_clust)

for (c in seq(n_clust)){
    clust<-da[da$"clust"==c,]
    mean_dist<-mean(clust$"dist")
    sd_dist<-sd(clust$"dist")
    clust_means[c]<-mean_dist
    clust_sd[c]<-sd_dist
}

top_10<-order(clust_means)[1:10]
for (c in top_10){
    cat("Cluster: ",c,", mean distance: ",clust_means[c],",sd: ",clust_sd[c],"\n",sep="")
    cwords(da,c)
}

# Now, let's plot some histograms.
cat("Plotting histograms!\n")
pdf(paste("hists_",n_clust,".pdf",sep=""))
par(mfrow=c(2,1))
hist(da$"dist",breaks=50,col="palegreen3",main=paste("Histogram of distance to centroid (n_clust =",n_clust,")"),xlab="Point-centroid distance")
hist(clust_means,breaks=50,col="deepskyblue2",main=paste("Histogram of mean point-centroid distance in cluster (n_clust =",n_clust,")"),xlab="Mean point-centroid distance in cluster")
dev.off()
