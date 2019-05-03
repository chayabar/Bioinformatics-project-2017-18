library(data.table)
#tree <- fread("MyData.csv")
#tree<-read.csv(file="MyData.csv",header=TRUE,sep=",");
GlobalSum<-tree[8583,3:ncol(tree)]
oligo<-c(1:ncol(GlobalSum))
plot(oligo,GlobalSum,type='h',ylim=c(0,1300))
#barplot(as.matrix(m))
