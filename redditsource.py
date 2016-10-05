## Fetch reddit images

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
    

