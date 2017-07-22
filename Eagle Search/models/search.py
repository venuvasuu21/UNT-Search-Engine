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
from applications.unt_searchengine.modules.search_index import inverted_index

#Path for documents dataset
class search:
    
    path = os.path.join(request.folder,'static','data\\')
    db = DAL('sqlite://unt_web.sqlite', pool_size=0,migrate=False)
    #tokens=Homework1.readDir(path,True);
    docsLen=len(os.listdir(path));
    
    def invertIndexDocs(self):
        '''invertIndex=dict();
        for filename in os.listdir(self.path+'unt_content\\'):
            terms=Tokeniser().tokeniseText(self.path+'unt_content\\'+filename, True,True);                   
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
            invertIndex.get(term)[0]=math.log(self.docsLen/invertIndex[term][0],2);'''
        invertIndex=inverted_index;
        return invertIndex;
    
    def calulateDocLens(self,invertIndexDict):
        docLens=dict();
        for docList in invertIndexDict.values():
            idf=docList[0];
            for doc,tf in docList[1].items():
                docLens[doc]=docLens.get(doc,0)+math.pow(idf*tf,2);
    
        for doc,idfs in docLens.items():
            docLens[doc]=math.sqrt(idfs);
        return docLens;
    
    def retrievalDocsOnQuery(self,query,invertedIndex):
        queryWords=Tokeniser().tokeniseText(query, False,True);
        simTable=dict();
        queryLength=0;
        maxTF=1;
        if len(queryWords)>=1:
            maxTF=self.topNWordsinVocab(queryWords, 1).popitem()[1];
        for qWord, qWordLen in queryWords.items():
            #idf=0
            if qWord in invertedIndex.keys():
                qWordLen=qWordLen/maxTF;
                idf=invertedIndex[qWord][0];
                docList=invertedIndex[qWord][1];
                queryLength=queryLength+math.pow(idf*qWordLen,2);
                for doc, tf in docList.items():
                    simTable[doc]=simTable.get(doc,0)+(tf*idf)*(qWordLen*idf);
        queryLength=math.sqrt(queryLength);
        docLenTable=self.calulateDocLens(invertedIndex);
        for doc in simTable.keys():
            docLen=docLenTable.get(doc);
            simTable[doc]=simTable[doc]/(docLen*queryLength);
        return simTable;
    
    def rankRetrievedDocs(self,simTable,n):
        rankedDocs=list();
        sortedDocs=list();
        for key, val in simTable.items():
            sortedDocs.append((val,key));
    
        sortedDocs.sort(reverse=True);
        for key, val in sortedDocs[:n]:
            file_path=val
            rankedDocs.append(file_path);
        return rankedDocs;
    
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
    
    def search_for_text(self,ii,text):
        #ii=self.invertIndexDocs(self.path);
        simTable=self.retrievalDocsOnQuery(text,ii);
        rankedAllDocs=self.rankRetrievedDocs(simTable, len(simTable));
        rankedList=self.loadURLsFromDB(rankedAllDocs)
        return rankedList
    
    def loadURLsFromDB(self, pageList):
        self.db.define_table('Pages',
                Field('url', type='text', length=2000, required=True, unique=True),
                Field('title', type='text'),
                Field('level', type='integer', length=3),
                Field('is_retrieved',type='integer', length=2),
                Field('error',type='integer', length=20),
                redefine=True
                )
        rankedList=list();
        for urll in pageList:
            row=self.db(self.db.Pages.id==int(urll)).select()
            #cur.execute('SELECT url FROM Pages where id=?',(int(id),))
            rankedList.append((row[0].url, row[0].title));
        return rankedList
