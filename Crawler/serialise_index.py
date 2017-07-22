'''
Created on Feb 7, 2016

@author: Venugopal Gonela
@ID: 11081500
@Description: This code creates inverted index of words with or without stemming based on "stemFlag"
#by reading documents from the cranfieldDocs folder and answers the questions in assignment2.
'''

from __future__ import division
import platform
import os
import math
import collections
from Tokeniser import Tokeniser
import sqlite3
import pickle


#Path for documents dataset
class search:
    
    if platform.system() is 'Windows':
        path='unt_content\\'
    else:
        path='unt_content/'
    
    #tokens=Homework1.readDir(path,True);
    docsLen=len(os.listdir(path));
    
    def invertIndexDocs(self):
        invertIndex=dict();
        for filename in os.listdir(self.path):
            terms=Tokeniser().tokeniseText(self.path+filename, True,True);                   
            maxTF=1;
            if len(terms)>1:
                maxTF=self.topNWordsinVocab(terms, 1).popitem()[1];
            for term,tf in terms.items():
                fileNum=int(filename);
                if term in invertIndex.keys():
                    docsList=invertIndex.get(term)[1];
                    docsList[fileNum]=docsList.get(fileNum,0)+tf/maxTF;
                    invertIndex.get(term)[1]=docsList;
                    invertIndex.get(term)[0]=len(invertIndex.get(term)[1]);
                else:
                    termDocFreq=dict();
                    termDocFreq[fileNum]=tf/maxTF;
                    docList=list();
                    docList.append(1);
                    docList.append(termDocFreq);
                    invertIndex[term]=docList;
        
        for term in invertIndex.keys():
            invertIndex.get(term)[0]=math.log(self.docsLen/invertIndex[term][0],2);
        return invertIndex;
    
    def topNWordsinVocab(self,terms,n):
        topWords=dict();
        termList=list();
        for key, val in terms.items():
            termList.append((val,key));
            
        termList.sort(reverse=True);
        i=0;
        for key, val in termList[:n]:
            i=i+1;
            #print(i,val,key);
            topWords[val]=key;
            
        return topWords;
    
if __name__=='__main__':

    invertIndex=search().invertIndexDocs()
    output = open('unt_index.pkl', 'wb')

    pickle.dump(invertIndex,output)
    
    output.close()