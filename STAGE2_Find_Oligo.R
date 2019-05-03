#chaya barbolin
#project oligoInViruses
#stage 2, input: DB of viruses, output: MyData.csv, the file conatains potential oligos in column names,
# in raws names the viruses name, the file show index of the apearance of potential oligo in virus
DownloadSquences<-function()
{
  print("need to do ftp")
}

FindStartEnd<-function()
{

  #directory to folder of seqs files
  SeqList<-list.files(path=paste(getwd(),"/DB  of all viruses", sep=""))
  cat("names of seqs files: ",SeqList, "\n")
  #size of gap can be changed
  size_gap<<-10
  OligoOptions=c("")
  
  #working on prepared sequence file
  fileName <- file.path(getwd(), "DB  of all viruses", "special seq.fasta")
  handle <- file(fileName,open="r")
  cat("making oligo samples from this:",readLines(handle, n=1),"\n")
  NowSeq=paste(readLines(handle), collapse="")
  close(handle)
  i=1
  cat("lenght of the query is:", nchar(NowSeq),'\n')
  while(i+size_gap-1<=nchar(NowSeq))
  {
    newOligo=substr(NowSeq,i,i+size_gap-1)
    #check to avoid duplicate oligos
    if (!newOligo %in% OligoOptions)
    {
      OligoOptions <- c(OligoOptions,newOligo)
    }
    i=i+1
  }
  #write all options for oligo to csv
  write.table(OligoOptions, file = "MyData.csv",eol=",",  row.names = FALSE, col.names = FALSE)
  size <<- length(OligoOptions)  #static value, the access to "size" is available in all program
  cat("number of oligos:", size)
  NumberSeq=length(SeqList)
  counter=0
  for (seq in SeqList)
  {
    i=1
    if(counter%%10==0)
      cat("already did ", counter, "of ",NumberSeq, "\n")
    counter=counter+1
    #save index of oligo that exist in this seq
    Indexs=vector(mode="character", length=size)
    fileName <- file.path(getwd(), "DB  of all viruses", seq)
    handle <- file(fileName,open="r")
    SeqName=readLines(handle, n=1)
    #add the id number of this nucleotide seq
    Indexs[1]=substr(SeqName,2,12)
    print(Indexs[1])
    NowSeq=paste(readLines(handle), collapse="")
    close(handle)
    
    #go over the seq and find oligo
    while(i<nchar(NowSeq))
    {
      newOligo=substr(NowSeq,i,i+size_gap-1)
      if (newOligo %in% OligoOptions)
      {
        indexOfOligo=match(newOligo, OligoOptions)
        if(Indexs[indexOfOligo]=="")
        {
          Indexs[indexOfOligo]= i
        }
        else
        {
          #if apear more than once
          Indexs[indexOfOligo]=paste(Indexs[indexOfOligo], i)
        }
      }
      i = i + 1
    }
    #write the information to csv
    write.table("", file = "MyData.csv",sep="", append=TRUE, row.names = FALSE, col.names = FALSE)
    write.table(Indexs, file = "MyData.csv",append=TRUE , eol=",",  row.names = FALSE, col.names = FALSE)
  }
}


SumNumberOfOligoApearance<-function()
{
  #count for each oligo how many times apear in column(in all seqs)
  size=33229
  Indexs=vector(mode="integer", length=size-1)
  GlobalApearance=vector(mode="integer", length=size-1)
  df <- read.csv("MyData.csv", colClasses=c("character"))
  i=3
  while (i <= size)
  {
    list1 <- df[[i]]
    counter=0
    Globalcounter=0
    for (j in list1)
    {
      if(!is.na(j)&&(j!="") )
      {
        Globalcounter=Globalcounter+1
        counter=counter+length(unlist(strsplit(j, " ")))
      }
    }
    GlobalApearance[i-1]=Globalcounter
    Indexs[i-1]=counter
    i=i+1
  }
  print(GlobalApearance)
  write.table("", file = "MyData.csv",sep="", append=TRUE, row.names = FALSE, col.names = FALSE)
  write.table("sum", file = "MyData.csv", append=TRUE,eol=",", row.names = FALSE, col.names = FALSE)
  write.table(Indexs, file = "MyData.csv",append=TRUE , eol=",",  row.names = FALSE, col.names = FALSE)
  write.table("", file = "MyData.csv",sep="", append=TRUE, row.names = FALSE, col.names = FALSE)
  write.table("GlobalSum", file = "MyData.csv", append=TRUE,eol=",", row.names = FALSE, col.names = FALSE)
  write.table(GlobalApearance, file = "MyData.csv",append=TRUE , eol=",",  row.names = FALSE, col.names = FALSE)
}

#DownloadSquences()
#FindStartEnd()
#SumNumberOfOligoApearance()
#datafile <- read.csv(paste(getwd(),"/MyData.csv", sep=""), header=T, sep=",")
#dim(datafile)
