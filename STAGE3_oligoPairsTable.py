#chaya barbolin
#project oligoInViruses
#stage 3, input file: NewData.csv (from stage 2),
#create table of the combination of oligos- pairs,
#for each virus if the pair oligo exist in the term, mention the distance and indexess

import csv
from collections import deque
import pandas as pd
import time

#make small table with less information for more faster results
#input full table, output part of the full table


def smallTableCutOff(): 
    cutoff=200 
    with open('NewData.csv', 'rb') as csvfile:
        lastLine=(deque(csv.reader(csvfile), 1)[0]) #the sum line, sum for every oligo
        #get the indexs of oligo higher than cutoff
        indexes = [i for i,x in enumerate(lastLine) if x.isdigit() and int(x) >cutoff] 
        print 'number of oligos after cutoff ', len(indexes)
        csvfile.seek(0) 
        reader = csv.reader(csvfile)
        for row in reader: #get the relevant data, only the column of indexes
            content = list(row[i] for i in [0,1]+indexes)
            with open('SmallData.csv', 'a') as smallData:
                smallData.write(','.join(content)+'\n')


#make table of pairs oligo, the distances for each virus
#input full/partial table of oligos and viruses, output: number of files Mypout..
def oligoPairsTable():
    df=pd.DataFrame()
    try:
        with open('SmallData.csv', 'rb') as csvfile:  
            reader = csv.reader(csvfile)
            colNames=(reader.next())[2:]
            #print 'col ', colNames
            rowNum=0
            for row in reader:
                virusName=row[1]
                line=row[2:]
                if virusName!='0':
                #print line
                    print virusName
                    for numOligo in range(0,len(line)):
                        current_oligo=(line[numOligo]).split(' ') #turn to another format
                        if current_oligo!=['']:
                            for apearanceOligo in range(0, len(current_oligo)):
                                if current_oligo[apearanceOligo]!='':
                                    #print 'the', numOligo,':',current_oligo[apearanceOligo]
                                    for numCompareOligo in range(numOligo,len(line)):
                                        if numCompareOligo==numOligo and apearanceOligo<len(current_oligo):
                                            compare_oligo=current_oligo[apearanceOligo: len(current_oligo)+1]
                                        else:
                                            compare_oligo=(line[numCompareOligo]).split(' ')
                                        if compare_oligo!=['']:
                                            for compare_apearance_oligo in compare_oligo:
                                                if compare_apearance_oligo!='':
                                                    dis=abs(int(current_oligo[apearanceOligo])-int(compare_apearance_oligo))
                                                    if(dis >= 500 and dis <= 1500):
                                                        #print colNames[numOligo], '-',colNames[numCompareOligo],':', 'distance=', dis, current_oligo[apearanceOligo], compare_apearance_oligo
                                                        name=str( colNames[numOligo] )+'-'+ str( colNames[numCompareOligo])
                                                        if not name in df.columns:
                                                            df[name]=''
                                                        if not virusName in df.index:
                                                            df.loc[virusName]=''
                                                        if df.at[virusName,name]=='':
                                                            df.at[virusName,name]=[{dis: (int(current_oligo[apearanceOligo]), int(compare_apearance_oligo))}]
                                                        else:
                                                            df.at[virusName,name]=df.at[virusName,name]+[{dis: (int(current_oligo[apearanceOligo]), int(compare_apearance_oligo))}]
                rowNum=rowNum+1
                if rowNum%1000==0:
                    fileName='Myout'+str(rowNum/1000)+'.csv'
                    with open(fileName, 'w') as f:
                        df.to_csv(f)
                        df=pd.DataFrame(columns=df.columns)
            df.to_csv('MyoutLast.csv')

    except:
        #e = sys.exc_info()[0]
        print 'error'
        fileName='Myout'+str(rowNum/1000)+'.csv'
        with open(fileName, 'w') as f:
            df.to_csv(f)

#------------------------main-----------------------------------
            
start = time.time()
##smallTableCutOff()
##oligoPairsTable()
print 'It took', time.time()-start, 'seconds.'
