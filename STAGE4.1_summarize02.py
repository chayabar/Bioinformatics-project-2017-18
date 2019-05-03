#chaya barbolin
#project oligoInViruses
#make one table for the output of stage 3, calculate the approximate min group of oligos 

import csv
import os
import pandas as pd
numCol=0
numRows=0
import time
start = time.time()
#///////////////////////not for use///////////////////////////////////////////////////////////////////////////////////////
#-------------------------clean data-------------------------
def cleanData():
    filename="Myout1.csv"
    df=pd.read_csv(filename)
    df=df.replace(to_replace='Nan', value='')
    df.to_csv(filename,index=False)

#------------------------see sizes---------------------------
def Sizes():
    prefixedFiles = [filename for filename in os.listdir('.') if filename.startswith("Myout")]
    for file_name in prefixedFiles:
        df=pd.read_csv(file_name)
        print file_name
        print 'rows=', len(df.index),'. columns=',len(df.columns)
#/////////////////////end///////////////////////////////////////////////////////////////////////////////////////////////////

#------------------------one table summarize------------------
#turn the output of stage 3 to 1 file
#input Myout.. files, output 'summarize.csv'
def OneTableOligoPairs():
    prefixedFiles = [filename for filename in os.listdir('.') if filename.startswith("Myout")]

    with open(prefixedFiles[-1], 'rb') as csvfile: #MyoutLast
        reader = csv.reader(csvfile)
        colNames=reader.next()
        numCol=len(colNames)
        
        with open('summarize.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(colNames)
            for file_name in prefixedFiles:
                with open(file_name, 'r') as r:
                    readerR = csv.reader(r)
                    info=readerR.next()
                    for info in readerR:
                        numRows=numRows+1
                        writer.writerow(info+[""]*(numCol-len(info))) #all data in standart sizes
    print 'rows=', numRows,'. columns=',numCol

#----------------------------------------------------------------------
#input table of pairs oligo
#output: finishViruses.txt -> for each round the oligo pair added and the viruses that have this pair
#description.txt -> number of round and how much viruses have been handled to this point
def findFinalOligos():
    finished=0 #boolian to mark weather we finished
    currentCsv='fixedSummarize.csv' #the file with oligo pairs
    roundNum=0

    summ=list() #list to hold the number of viruses to each pair oligo
    numCol=0
    with open(currentCsv, 'rb') as r: #count for each oligo pair the virues have that oligo pair

        readerR = csv.reader(r)
        info=readerR.next()
        numCol=len(info)
        summ=[0]*len(info) #all zero
        print len(info)
        for info in readerR:
            #print len(info)
            for i in range(0, len(info)):
                if info[i]!='' and i!=0 :
                    summ[i]=summ[i]+1 #if the virus have this oligp pair , add to summ

    finishedViruses=list()  # hold the viruses that been handled      
    while not finished: #while not all viruses have olig pair
        roundNum+=1
        chosenViruses=list() #the viruses that chosen at this round
        minusSum=[0]*numCol #the count of apearance in oligo pair in viruses we drop this round
        with open(currentCsv, 'rb') as r:
            readerR = csv.reader(r)
            info=readerR.next() #get first raw (raw of oligo pairs)
            pos_max=summ.index(max(summ[1:])) #find the max for this point
            oligoPair=info[pos_max] #get name of oligo pair with max apearance in virus DB
            print oligoPair #chosen oligo pair
            print 'summ[pos_max]', summ[pos_max] #print number of apearance
            if summ[pos_max]==0: #if 0 viruses apear for the max oligo pair , mission completed
                finished=1
                print "finished"
                pass
            else: 
                for info in readerR:
                    virusName_apear=[info[0] ,info[pos_max]] #get the virus name and the info in the chosen oligo Pair
                    if virusName_apear[1]!='' and virusName_apear[0] not in finishedViruses: #in case this virus have the chosen oligo pair
                        chosenViruses.append(virusName_apear[0]) #add the virus to list of chosen viruses
                        finishedViruses.append(virusName_apear[0]) #sdd to finished viruses
                        for i in range(0, len(info)): #count the apearance of oligo pairs of the chosen viruses 
                            if info[i]!='' and i!=0:
                                minusSum[i]=minusSum[i]+1                
                        #print 'added to viruses'
                #write results to files
                fh=open("finishViruses.txt", "a") 
                fh.write('%s :number of viruses=%4d' %(oligoPair, summ[pos_max]))
                fh.write('\n')
                fh.writelines(["%s\n" % item  for item in chosenViruses])
                fh.write("----------------\n")
                fh.close()
                summ=[a_i - b_i for a_i, b_i in zip(summ,minusSum)] #update the summ acording to the chosen viruses we dismiss from count
                fh=open("descriptionRun.txt", "a")
                fh.write('round number(oligo pair sum):%4d viruses sum:%4d' %(roundNum, len(finishedViruses)))
                fh.write('\n')
                fh.close()

    duration= time.time()-start
    print 'It took', duration, 'seconds.'
    fh=open("descriptionRun.txt", "a")
    fh.write('duration:%4d' %(duration))
    fh.write('\n')
    fh.close()
    #[i for i, j in enumerate(summ) if j == myMax]
