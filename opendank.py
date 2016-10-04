#!/usr/bin/python2

import praw
r = praw.Reddit(user_agent='opendank')
submissions = r.get_subreddit('pics').get_hot(limit=5)
for x in submissions:
    print(x)
