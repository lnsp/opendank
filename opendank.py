#!/usr/bin/python2
import os
import glob
import datetime
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
        if "i.imgur.com/" in x.url or "i.reddituploads.com/" in x.url:
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

def clean_up():
    for filename in glob.glob("image*"):
        os.remove(filename)

def display_image(panel, name):
    photo = Image.open(name)
    photo.thumbnail((window.winfo_width(), window.winfo_height()), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(photo)
    panel.configure(image = img)
    panel.image = img

def update_window():
    global active_id
    global last_check_date
    global images

    current_date = datetime.date.today()
    if current_date.day != last_check_date.day:
        clean_up()
        images = fetch_images()
        last_check_date = current_date

    active_id = (active_id + 1) % len(images)
    display_image(panel, images[active_id])
    window.after(1000, update_window)

last_check_date = datetime.date.fromtimestamp(0)
active_id = 0
images = []
window, panel = create_window()
update_window()
window.mainloop()

