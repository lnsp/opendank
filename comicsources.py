##HTMLsources

from bs4 import BeautifulSoup
import urllib2

class HtmlSource:
    def get_soup(self, url):
        
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        html_doc = urllib2.urlopen(req)
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

    def fetch_images():
        raise Exception('Abstract class: Don\'t use!!!')
    

class XkcdSource(HtmlSource):
    
    def fetch_images(self):
        urls = []
        soup = self.get_soup('http://www.xkcd.com/')
        for content in soup.find_all('div'):
            if content.get('id') == 'comic':
                for image in content.find_all('img'):
                    urls.append('http:' + image.get('src'))
        return urls


class SysadminotaurSource(HtmlSource):
    
    def fetch_images(self):
        urls = []
        soup = self.get_soup('http://sysadminotaur.com/')
        for content in soup.find_all('img'):
            if content.get('name') == 'main':
                urls.append('http://sysadminotaur.com/' + content.get('src'))
        return urls
