"""sources module provides URL extraction utilities for images from the WWW."""
from bs4 import BeautifulSoup
import requests
import praw


class Reddit(object):
    """Reddit can fetch image urls from your favorite subreddit."""

    # pylint: disable=too-few-public-methods

    def __init__(
            self,
            subreddit="pics",
            valid_hosts=None,
            max_items=20):
        if valid_hosts is None:
            valid_hosts = [
                "i.imgur.com/",
                "i.reddituploads.com/",
                "i.redd.it/"]

        self.subreddit = subreddit
        self.valid_hosts = valid_hosts
        self.max_items = max_items
        self.client = praw.Reddit(user_agent="opendank")

    def fetch_images(self):
        """Fetch images from subreddit."""
        images = []

        hot_submissions = self.client.get_subreddit(
            self.subreddit).get_hot(limit=self.max_items)
        for submission in hot_submissions:
            if any(host in submission.url for host in self.valid_hosts):
                images.append(submission.url)
        return images


class HtmlSource(object):
    """HtmlSource can fetch a generic html request. Use this as a template for
    your own sources."""

    # pylint: disable=no-self-use

    def get_soup(self, url):
        """Get a bowl full of HTML soup."""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def fetch_images(self):
        """Fetch image URLs from the HTML source."""
        raise Exception("This is a template class, you should not use this method.")


class CustomSource(HtmlSource):
    """CustomSource parses a HTML source based on a descriptive selection string."""

    def fetch_source(self, selection, tokens):
        """Uses the tokens to find something valuable in the selection."""
        results = []
        if tokens[0] == ">":
            for element in selection.find_all(tokens[1]):
                results += self.fetch_source(element, tokens[2:])
        elif tokens[0] == ":":
            attribute = tokens[1]
            tokens = tokens[3:]
            valid_qualifiers = []

            while tokens[0] not in [">", "!"]:
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
        self.tokens = pattern.split(" ")

    def fetch_images(self):
        soup = self.get_soup(self.tokens[0])
        return self.fetch_source(soup, self.tokens[1:])
