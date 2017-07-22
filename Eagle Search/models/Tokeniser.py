#Author: Venugopal Gonela
#ID:11081500
#This code creates dictionary of words with or without stemming based on "stemFlag"
#by reading documents from the path specified and answers the questions in assignment1.

import os
import re
import platform
from applications.unt_searchengine.modules.porter_stemmer import PorterStemmer

class Tokeniser:
    
    #Path for documents dataset
    path = os.path.join(request.folder,'static','data\\')
    
    #Extract terms from the documents in a directory and calculates terms frequencey
    #stemFlag=True for stemming of words and stop words removal
    def tokeniseText(self,doc,isFile,stemFlag):
        stemmer=PorterStemmer();
        tokens=dict();
        stopWords=self.loadStopWords();
        fh=list()    
        if isFile is True:
            fh=open(doc);
        else :
            fh.append(doc)
        for line in fh:        
            line=re.sub('(<.*>)','',line);
            line=re.sub('[^0-9a-zA-Z]+',' ',line);
            line=line.strip().lower();
            words=line.split();
            if stemFlag is True :
                for word in words:
                    if word not in stopWords:
                        word=stemmer.stem(word,0,len(word)-1);
                        if len(word)>1 and word not in stopWords:
                            tokens[word]=tokens.get(word,0)+1;
            else:
                for word in words:
                    if len(word)>1:
                        tokens[word]=tokens.get(word,0)+1;                    
        return tokens
    
    #Loading stop words into memory
    def loadStopWords(self):
        p=os.path.join(request.folder,'static','data\\stopwords.txt')
        handle=open(p);
        stopWords=list();
        for line in handle:
            stopWords.append(line.rstrip());
        return stopWords
