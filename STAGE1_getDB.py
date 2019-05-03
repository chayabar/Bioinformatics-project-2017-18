#chaya barbolin
#project oligoInViruses
#stage 1, input file: viruses.csv (dowloaded from ftp ncbi),
#extract the ids of viruses and download them to directory DB_Viruses- create the virus DB: OUTPUT


import csv
from ftplib import FTP
#Download sequences from NCBI
from Bio import Entrez
from Bio import SeqIO
#Using records
from Bio.Blast import NCBIWWW
import tkFileDialog
import tkMessageBox
import winsound
from Bio.Blast import NCBIXML
from StringIO import StringIO
import numpy as np
import panda as pd
from Tkinter import *
import string
import os

def download_seq(SequenceID):
    Entrez.email = "A.N.Other@example.com"  #change to real address to get messages (about problems, warnning)
    
    handle = Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id=SequenceID)  #download through entrz the sequence
    Sequence = SeqIO.read(handle, "fasta") 
    handle.close()

    save_path=os.path.dirname(os.path.abspath(__file__))+r"\DB of all viruses"  #path to save the file in results
    if not os.path.exists(save_path):  #if folder not exist, create it
        os.makedirs(save_path)
    completeName = os.path.join(save_path, SequenceID+".fasta") 
    
    save_file = open(completeName, "w")  #open for write
    SeqIO.write(Sequence,completeName,"fasta")
    save_file.close()

    print SequenceID," was downloaded"


def getIDtoFile(): #extract ids fron viruses file
    coloumnOfID=9  #the ID is in column 9
    IDList=[]
    with open("viruses.csv", "r") as infile:
        CSVreader = csv.reader(infile)
        for line in CSVreader:
            infoWithID=line[coloumnOfID]
            listOfInfo=infoWithID.split(":")
            boolian=0
            for i in listOfInfo:
                if boolian!=0:
                    IDList+=[i[0:11]]
                boolian=1
    with open("IDlist.txt", 'wb') as ListOfID: #write all ids to file 
        for item in IDList:
            ListOfID.write("%s\n" % item)

##getIDtoFile()

with open("IDlist.txt", 'r') as ListOfID:
    for line in ListOfID:
        download_seq(line.strip('\n'))








    

