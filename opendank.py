#!/usr/bin/python2
import praw
import requests
import Tkinter as tk
from PIL import ImageTk, Image

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

def display_image(name):
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.title('opendank')

    img = ImageTk.PhotoImage(Image.open(name))
    panel = tk.Label(window, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")

    window.mainloop()

image_count = fetch_images()
display_image('image' + str(image_count-1))

