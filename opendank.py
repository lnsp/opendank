#!/usr/bin/python2
import praw
import requests
from PIL import Image

def fetch_images():
    r = praw.Reddit(user_agent='funny')
    submissions = r.get_subreddit('pics').get_hot(limit=20)
    imageId = 0
    for x in submissions:
        if "i.imgur.com/" in x.url:
            response = requests.get(x.url)
            if response.status_code == 200:
                with open("image" + str(imageId), 'wb') as img:
                    for chunk in response.iter_content(4096):
                        img.write(chunk)
                imageId += 1
    return imageId

fetch_images()

