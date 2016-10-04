#!/usr/bin/python2
import praw
import requests
import Tkinter as tk
import time
from PIL import ImageTk, Image

def fetch_images():
    r = praw.Reddit(user_agent='funny')
    submissions = r.get_subreddit('pics').get_hot(limit=20)
    image_names = []
    imageId = 0
    for x in submissions:
        if "i.imgur.com/" in x.url:
            response = requests.get(x.url)
            if response.status_code == 200:
                with open("image" + str(imageId), 'wb') as img:
                    for chunk in response.iter_content(4096):
                        img.write(chunk)
                image_names.append('image' + str(imageId))
                imageId += 1
    return image_names

def create_window():
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.title('opendank')

    panel = tk.Label(window)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    return window, panel

def display_image(panel, name):
    img = ImageTk.PhotoImage(Image.open(name))
    panel.configure(image = img)
    panel.image = img

def update_window():
    global active_id
    active_id = (active_id + 1) % len(images)
    display_image(panel, images[active_id])
    window.after(1000, update_window)

last_check_date = 0
active_id = 0
images = fetch_images()
window, panel = create_window()
update_window()
window.mainloop()

