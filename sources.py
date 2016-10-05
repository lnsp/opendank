from bs4 import BeautifulSoup
import urllib2
import praw

class RedditSource:
    def __init__(self, subreddit='pics', valid_hosts=['i.imgur.com/', 'i.reddituploads.com/', 'i.redd.it/'], max_items = 20):
        self.subreddit = subreddit
        self.valid_hosts = valid_hosts
        self.max_items = max_items
        self.client = praw.Reddit(user_agent='opendank')

    def fetch_images(self):
        images = []

        hot_submissions = self.client.get_subreddit(self.subreddit).get_hot(limit=self.max_items)
        for submission in hot_submissions:
            if any(host in submission.url for host in self.valid_hosts):
                images.append(submission.url)
        return images

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
