##This code read protein annotation/classification file and split the Uniprot Ids to create gene name and protein name columns.

import sys
import re
import argparse
import pandas as pd

def readFile(filename, sep, headerFlag):
    if headerFlag==0:
        fileDFObj = pd.read_table(filename, sep=sep, keep_default_na=False, na_values=[''])
    elif headerFlag==1:
        fileDFObj = pd.read_table(filename, sep=sep, header=None, keep_default_na=False, na_values=[''])
    else:
        print("Unrecognized Header Flag")
    return fileDFObj;
def main(annotationFile, outFile):
    annotation = readFile(annotationFile, ',',0)
    #subDF=annotation['Protein ID'].str.extract(".+?\|(.+)?\|([^ ]+) (.+)? OS=.+? GN=([^ ]+)(?: |$)")
    subDF=annotation['Protein ID'].str.extract("(.+)?\|(.+)?\|([^ ]+) (.+)? OS=.+? GN=([^ ]+)(?: |$)|(.+)?\|(.+)?\|([^ ]+) (.+)? OS=.+?")
    subDF[pd.isnull(subDF)]='-'
    #as I have used '|' for the regex, all together it will have 9 columns for each row. Results would either be in first 5 columns or last 4.
    subDFA=subDF[subDF[0]!="-"]
    subDFB=subDF[subDF[0]=="-"]
    annotationA=annotation[subDF[0]!="-"]
    annotationB=annotation[subDF[0]=="-"]
    annotationA['Protein ID']=subDFA[1]
    annotationA['Protein Name']=subDFA[2]
    annotationA['Gene Name']=subDFA[4]
    annotationA['Protein description']=subDFA[3]
    annotationA['Source']=subDFA[0]
    
    annotationB['Protein ID']=subDFB[6]
    annotationB['Protein Name']=subDFB[7]
    annotationB['Gene Name']='N/A'
    annotationB['Protein description']=subDFB[8]
    annotationB['Source']=subDFB[5]
    annotation=pd.concat([annotationA,annotationB])
    #outFile=annotationFile.replace("_annotation","_details_annotation")
    #print(outFile)
    annotation.to_csv(outFile, index=False)
    
parser = argparse.ArgumentParser(description='Fasta file filtering based on a header list given')
parser.add_argument("-a","--annot", required=True, help="ORFs fasta file name")
parser.add_argument("-o","--out", required=True, help="ORFs fasta file name")

args = parser.parse_args()

main(args.annot, args.out)

#annotationFile="C:/Users/shyama/Dropbox/OliverData/Annotation/G10.assemblies.fasta.transdecoder.pep_annotation.csv"