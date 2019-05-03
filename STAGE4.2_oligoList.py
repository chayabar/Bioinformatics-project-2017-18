#chaya barbolin
#project oligoInViruses
#order the results, get the oligo group clearly
import csv
with open('finishViruses.txt', 'r') as r: #read the information
    content= r.readlines()
oligoCollection=[] #list to hold the oligo in final group
for line in content: #for each line
    if line.find('number')>=0: #line of information about the oligo choice
        pairOligo=line.split()[0] #get the oligo pair
        pairoligo_list=pairOligo.split('-') #split to 2 seperate oligos
        #if not in the final group , add
        if pairoligo_list[0] not in oligoCollection: 
            oligoCollection.append(pairoligo_list[0])
        if pairoligo_list[1] not in oligoCollection:
            oligoCollection.append(pairoligo_list[1])

fh=open("oligo_list.txt", "w") #write the final oligo group to file
fh.writelines(["%s\n" % item  for item in oligoCollection])
fh.write("total oligos: %4d\n" %len(oligoCollection))
fh.close()
