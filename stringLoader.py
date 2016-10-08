from bs4 import BeautifulSoup
import urllib2
import diashow
from sources import HtmlSource



class configSource(HtmlSource):
    def check_content(self, i, stringArray, mycontent):
        results = []
        x = i
        print 'x = ' , x
        print stringArray[i], 'starting'
        for content in mycontent.find_all(stringArray[i]):
            i += 1
            
            runner = True 
            while (stringArray[i] == ',' or stringArray[i] == '('):
                print stringArray[i+1]
                print stringArray[i+2]
                print content.get(stringArray[i+1])
                print stringArray[i+3]
                print '------'
                
                if(stringArray[i+3] == 'x'):
                    results += content.get(stringArray[i+1])
                    print "angekommen"
                    print content.get(stringArray[i+1])
                
                if (not(content.get(stringArray[i+1]) == stringArray[i+3] )):##and content.get(stringArray[i+2]) == "=" )):
                    runner = False
                    print 'not ok'
                else:
                    print 'ok'
                i += 4
            print i
            if stringArray[i] == ')':
                print "da"
                if runner and i < len(stringArray):
                    print "finale"
                    
                    results += self.check_content(i+1,stringArray,content)
            else:
                raise Exception('Klammer zu vergessen')

            i = x
            
        return results
            
    
    def process_line (self,line):
        stringArray = line.split(' ')
        print stringArray
        soup = self.get_soup(line)
        i = 1
        self.check_content(i,stringArray,soup)

    def get_soup(self, url):
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        html_doc = urllib2.urlopen(req)
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup
                
    def __init__ (self):
        print 'hi'
        
s = configSource()

s.process_line('http://www.xkcd.com/ div ( id = comic ) img ( src = x )')

##f = open('testCFG.txt', 'r')
##for line in f:
##        process_line(line)
        
