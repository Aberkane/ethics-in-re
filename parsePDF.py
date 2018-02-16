# Based on: https://github.com/adityashrm21/Pdf-Word-Count
# Author: Aditya Sharma
# Adapted by Abdel Aberkane
# 
# Script that parses PDFs using textract and processes it further using Spacy. 
# The script can be executed by adding as argument in which the directory it should run.
# If no argument is given, the script will run in the script directory.
# The script will output a txt file with the frequency of noun chunks of the parsed PDFs.


import textract
import os, sys, glob
# import spacy
# import PyPDF2
import string
import en_core_web_sm
# import os
import errno

import collections
from sys import exit
# from itertools import chain
# from os.path import isfile, join
# from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nlp = en_core_web_sm.load()

def getFiles():
    # if no argument is given, script will run in script directory
    if len(sys.argv)==1:
        # extract script directory and list files in that directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        pdf_files = list()
    
        for filename in glob.glob("*.pdf"):
            pdf_files.append(filename)
            
        return pdf_files
    elif len(sys.argv)!=2:
        print('command usage: python parsePDF.py "C:\somedir\pdffiles\"')
	exit(1)
    else:
        pdfFile = sys.argv[1]
        path = sys.argv[1]
        
        # check if the specified directory exists or not
        try:
            if os.path.exists(pdfFile):
                pdf_files = list()
		print(path + " - file found!")
		os.chdir(path)
                for file in glob.glob("*.pdf"):
                    pdf_files.append(file)
        except OSError as err:
            print(err.reason)
            exit(1)
        return pdf_files

# def getFiles():
#         pdf_files = list()
#         
#         for filename in glob.glob("*.pdf"):
#             pdf_files.append(filename)
#         return pdf_files
#         
# 
# def getPageCount(pdf_file):
# 	pdfFileObj = open(pdf_file, 'rb')
# 	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# 	pages = pdfReader.numPages
# 	#text = textract.process(pdfFileObj, method='pdfminer')
# 	#print(text)
# 	return pages
# 
# 
# def extractData(pdf_file, page):
# 	pdfFileObj = open(pdf_file, 'rb')
# 	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# 	pageObj = pdfReader.getPage(0)
# 	data = pageObj.extractText()
# 	return data
# 
# def getWordCount(data):
# 	data=data.split()
# 	return len(data)
# 	
def countItems(text, n):
        #List that includes both words and their frequency
        counter = collections.Counter(text)
        
        #sorted on most common words
        return(counter.most_common(n))
	
# extract text from pdf file	
def getText(doc):
	text = textract.process(doc)
	return text

def prepareText(text):
        text = text.split(" ")
        return text

def cleanText(text):
        stop_words = stopwords.words('english')
        text = [word.lower() for word in text if not word in stop_words and  not word in string.punctuation]
        return text

def getNounChunks(text):
        return [token.text.lower() for token in text.noun_chunks]

def getWords(text):
        return [token.text for token in text if token.is_stop != True and token.is_punct != True]

def writeFile(file, noun_chunks):
            output_file = "output/" + os.path.splitext(str(file))[0]+".txt"
            # print tmp
            # output_file = "output/classification.txt"
            
            if not os.path.exists(os.path.dirname(output_file)):
                try:
                    os.makedirs(os.path.dirname(output_file))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

    
            output = open(output_file,"w")  
            output.write(file + "\n") 

            for item in noun_chunks:
                output.write("%s\n" % str(item))
            output.close() 


def main():
        files = getFiles()

        for file in files:
            # extract text from pdf
            text = getText(file)

            # some spacy magic
            text = unicode((text).decode('utf8'))
            text = nlp(text)

            noun_chunks = getNounChunks(text)
            noun_chunks = countItems(noun_chunks, 50)

            writeFile(file, noun_chunks)
   
          

if __name__ == '__main__':
	main()