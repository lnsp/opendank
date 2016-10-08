from bs4 import BeautifulSoup
import requests
from sources import HtmlSource

class CustomSource(HtmlSource):
    def fetch_source(self, selection, tokens):
        results = []
        if tokens[0] == ">":
            for element in selection.find_all(tokens[1]):
                results += self.fetch_source(element, tokens[2:])
        elif tokens[0] == ":":
            for element in selection.find_all(attrs={tokens[1]: tokens[3]}):
                results += self.fetch_source(element, tokens[4:])
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
