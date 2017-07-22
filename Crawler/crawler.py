'''
Created on Mar 29, 2016

@author: venugopal
'''
import sqlite3
import Queue
import re
import traceback
from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
from urlparse import urlparse
import platform
import os

class crawler:
    
    def crawl(self):
        
        if not os.path.exists('unt_content/'):
            os.makedirs('unt_content/')
        path='unt_content/'
        conn=self.createDatabase();
        level=self.getLevelToStart();
        
        mainQueue = Queue.Queue()
        
        cur = conn.cursor()
        
        cur.execute('SELECT url FROM Pages where is_retrieved=0 and level=?',(level,))
        for row in cur:
            mainQueue.put(row[0])
        
        while level < 15:
            if mainQueue.empty():
                level+=1
                cur.execute('SELECT url FROM Pages where is_retrieved=0 and level=?',(level,))
                for row in cur:
                    mainQueue.put(str(row[0]))
                print "****************************Level:" , level,"******************************"
                if mainQueue.empty():
                    print "No more pages to crawl"
                    break;
            url=mainQueue.get()
            print level,url
            cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( url, ))
            page_id=cur.fetchone()[0]                
            try:
                html_page = urllib2.urlopen(url)
                if 'text/html' != html_page.info().gettype() :
                    print "Ignore non text/html page"
                    cur.execute('DELETE from Pages WHERE url=?', (url, ) )
                    conn.commit()
                    continue
                
                #self.save_html(html_page,page_id)
                soup = BeautifulSoup(html_page,"html.parser")
                title=soup.find('title').text
                [s.extract() for s in soup('style')]
                [s.extract() for s in soup('script')]
                text = soup.getText()
                text=re.sub('(\s)+', ' ', text)
                cur.execute('UPDATE Pages SET is_retrieved=1, title=?, content=? WHERE url=?', (title, text, url) )
                conn.commit()
                #adding key words
                keyText=url+' '+title
                keyText=re.sub('[^0-9a-zA-Z]+',' ',keyText);
                keyText=re.sub('(unt|UNT|edu|www|http|https|University of North Texas|htm|html|php)','',keyText)
                
                mod_text=keyText*10 +' '+text
                writeContent = open(path+str(page_id), "w")
                writeContent.write(mod_text.encode('utf-8'))
                
                        
            except:
                print "Unable to retrieve page",url
                cur.execute('DELETE from Pages WHERE url=?', (url, ) )
                conn.commit()
                continue
            try:
                for link in soup.findAll('a'):
                    aLink=link.get('href')
                    
                    if aLink is None:
                        continue
                    aLink = aLink.strip().lower() 
                    
                    if aLink.startswith(".."):
                        aLink = aLink.lstrip("..")                   
                    if aLink.startswith('mail') or aLink.startswith('#'):
                        continue
                    up = urlparse(aLink)
                    if ( len(up.scheme) < 1 ) :
                        aLink = urljoin(url, aLink)
                        up = urlparse(aLink)
                    
                    if up.netloc.startswith('m.') or 'unt.edu' not in up.netloc :
                        continue
                    
                    aLink=urljoin(aLink, up.path)
                    """if 'cse.unt' not in re.findall("//([^/]+)",aLink)[0]:
                        continue"""
                    ipos = aLink.find('#')
                    if ( ipos > 1 ) : aLink = aLink[:ipos]
                    aLink=aLink.strip("/")
                    #print aLink
                    up = urlparse(aLink)
                    cur.execute('INSERT OR IGNORE INTO Pages (url, is_retrieved, level, url2) VALUES ( ?, 0, ?, ? )', ( aLink,level+1, up.netloc+up.path) ) 
                    conn.commit() 
                    
            except:
                print "Error parsing page ",url
                traceback.print_exc()
                       
            if mainQueue.empty():
                level+=1
                cur.execute('SELECT url FROM Pages where is_retrieved=0 and level=?',(level,))
                for row in cur:
                    mainQueue.put(str(row[0]))
                print "****************************Level:" , level,"******************************"
                if mainQueue.empty():
                    print "No more pages to crawl"
                    break;
    
    
    def createDatabase(self):
        conn = sqlite3.connect('unt_web.sqlite')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Pages 
            (id INTEGER PRIMARY KEY, title TEXT, url TEXT UNIQUE, level INTEGER,  
             error INTEGER, is_retrieved INTEGER, url2 TEXT UNIQUE, content TEXT UNIQUE)''')
        
        cur.execute('SELECT count(*) FROM Pages where is_retrieved !=1')
        count=cur.fetchone()[0]
        if count==0:
            starturl = raw_input('Enter any url to start with or just hit enter: ')
            if ( len(starturl) < 1 ) : 
                cur.execute('INSERT OR IGNORE INTO Pages (url, is_retrieved, level, url2) VALUES ( ?, 0, ?, ? )', ('http://www.unt.edu',1,'www.unt.edu' ) )
                #cur.execute('INSERT OR IGNORE INTO Pages (url, is_retrieved, level, url2, new_rank) VALUES ( ?, 1, ?, ?, 1.0 )', ('https://my.unt.edu',1,'my.unt.edu' ) )
                #cur.execute('INSERT OR IGNORE INTO Pages (url, is_retrieved, level, new_rank, url2) VALUES ( ?, 0, ?, 1.0,? )', ('http://www.cse.unt.edu/site/index.php',1,'www.cse.unt.edu/site/index.php') )
                #cur.execute('INSERT OR IGNORE INTO Pages (url, is_retrieved, level, new_rank) VALUES ( ?, 0, ?, 1.0 )', ('http://www.cse.unt.edu/~ccaragea',1 ) ) 
                conn.commit()
            else:
                cur.execute('INSERT OR IGNORE INTO Pages (url, is_retrieved, level) VALUES ( ?, 0, ? )', (starturl,1 ) ) 
                conn.commit()
        return conn;
    
    def getLevelToStart(self):
        conn = sqlite3.connect('unt_web.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT level FROM Pages where is_retrieved=0 ORDER BY level')
        try:
            row = cur.fetchone()
            return row[0]
        except:
            return 1        

if __name__ == '__main__':
    
    c =crawler()
    c.crawl()