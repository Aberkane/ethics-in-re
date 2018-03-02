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
import spacy
# import PyPDF2
import string
import en_core_web_sm
# import os
import errno
import nltk
import re

import collections
from sys import exit
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS
#stop_words = nltk.download('stopwords')
#nlp = en_core_web_sm.load()

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


def countItems(text, n):
    #List that includes both words and their frequency
    counter = collections.Counter(text)
    
    #sorted on most common words
    return(counter.most_common(n))
	

# extract text from pdf file	
def getText(doc):
	try:
		text = textract.process(doc)
	except Exception as ex:
		print "Text extraction unsuccesfull .. switching to different method .. ",

		try:
			text = textract.process(doc, method='pdfminer')	
		except Exception as ex:
			print "text extraction successful"

	return text


def prepareText(text):
    text = text.split(" ")
    return text


def cleanText(text): 
	# get rid of newlines
	#text = text.strip().replace(u"\x0c", "").replace("\n", " ").replace(u"\u2018", "'").replace#(u"\u2019", "'").replace(",", "").replace("\r", " ").replace("- ", "")

	text = text.replace(u"\x0c", "").replace("-\n\n", "").replace("\n", " ").replace(u"\u2018", "'").replace(u"\u2019", "'").replace(",", "").replace("\r", " ").replace("- ", "")


	while '  ' in text:
    		text = text.replace('  ', ' ')



	# replace HTML symbols
#	text = text.replace("&amp;", "and").replace("&gt;", ">").replace("&lt;", "<")

	# lowercase
	text = text.lower()

	return text


def cleanChunks(noun_chunks):
	clean_chunks = list()

	for chunk in noun_chunks:	
		#print "chunk: " + chunk.text
		for token in chunk:
		#	print "new token: " + token.text
			if(token.is_stop):
				if(chunk.text != token.text):
					clean_chunks.append(chunk.text.replace("the ", "").replace("a ","").replace("an ", ""))
		#			print "flag1"
				break
			else:
				clean_chunks.append(chunk.text.replace("the ", "").replace("a ","").replace("an ", ""))
		#		print "flag2"
				break
		#print clean_chunks
		
	return clean_chunks


def getNounChunks(text):
	noun_chunks = text.noun_chunks
	noun_chunks = cleanChunks(noun_chunks)
	return noun_chunks


def getWords(text):
        return [token.text.lower() for token in text if token.is_stop != True and token.is_punct != True]

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
	nlp = spacy.load('en')
	counter = 1

	print "We will start parsing ..."
        for file in files:
	        print "# file " + str(counter) + ": " + file
	        # extract text from pdf
	        print "Parsing ...", 
	        text = getText(file)

	        #text = unicode((text).decode('utf8'))
	        text = unicode((text), errors = "ignore")
									
	        text = cleanText(text)
	        #print text	
	        #exit(0)
	        text = nlp(text)

	        print " successful.\nCalculating noun chunks ...", 
	        noun_chunks = getNounChunks(text)
	        #words = getWords(text)

	        noun_chunks = countItems(noun_chunks, 150)
	        #words = countItems(words, 150)

	        print " successful.\nWriting output file ...", 
	        writeFile(file, noun_chunks)
	        counter = counter + 1 
	        print "successful. \n"

if __name__ == '__main__':
	main()