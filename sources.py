from bs4 import BeautifulSoup
import requests
import praw


class Reddit:

    def __init__(
            self,
            subreddit='pics',
            valid_hosts=[
                'i.imgur.com/',
                'i.reddituploads.com/',
                'i.redd.it/'],
            max_items=20):
        self.subreddit = subreddit
        self.valid_hosts = valid_hosts
        self.max_items = max_items
        self.client = praw.Reddit(user_agent='opendank')

    def fetch_images(self):
        images = []

        hot_submissions = self.client.get_subreddit(
            self.subreddit).get_hot(
            limit=self.max_items)
        for submission in hot_submissions:
            if any(host in submission.url for host in self.valid_hosts):
                images.append(submission.url)
        return images


class HtmlSource(object):

    def get_soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def fetch_images(self):
        raise Exception('Abstract class: Don\'t use!!!')


class Xkcd(HtmlSource):

    def fetch_images(self):
        urls = []
        soup = self.get_soup('http://www.xkcd.com/')
        for content in soup.find_all('div'):
            if content.get('id') == 'comic':
                for image in content.find_all('img'):
                    urls.append('http:' + image.get('src'))
        return urls


class Sysadminotaur(HtmlSource):

    def fetch_images(self):
        urls = []
        soup = self.get_soup('http://sysadminotaur.com/')
        for content in soup.find_all('img'):
            if content.get('name') == 'main':
                urls.append('http://sysadminotaur.com/' + content.get('src'))
        return urls


class CustomSource(HtmlSource):

    def fetch_source(self, selection, tokens):
        results = []
        if tokens[0] == ">":
            for element in selection.find_all(tokens[1]):
                results += self.fetch_source(element, tokens[2:])
        elif tokens[0] == ":":
            attribute = tokens[1]
            tokens = tokens[3:]
            valid_qualifiers = []

            while tokens[0] not in ['>', '!']:
                valid_qualifiers.append(tokens[0])
                tokens = tokens[1:]

            for qualifier in valid_qualifiers:
                for element in selection.find_all(
                        attrs={attribute: qualifier}):
                    results += self.fetch_source(element, tokens)

        elif tokens[0] == "!":
            value = selection[tokens[1]]
            tokens = tokens[2:]
            while len(tokens) > 0:
                if tokens[0] == "prefix":
                    value = tokens[1] + value
                elif tokens[0] == "suffix":
                    value = value + tokens[1]
                tokens = tokens[2:]
            results += [value]
        return results

    def __init__(self, pattern):
        self.tokens = pattern.split(' ')

    def fetch_images(self):
        soup = self.get_soup(self.tokens[0])
        return self.fetch_source(soup, self.tokens[1:])
