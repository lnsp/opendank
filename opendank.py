#!/usr/bin/python2
import sys
import os
import glob
import datetime
import praw
import requests
import Tkinter as tk
import time
from PIL import ImageTk, Image

class ImageDiashow:
    def __init__(self, subreddit='earthporn', max_items=20, image_prefix='image', valid_hosts=['i.imgur.com/', 'i.reddituploads.com/', 'i.redd.it/'], update_interval=10000):
        self.update_interval = update_interval
        self.active = 0
        self.max_items = max_items
        self.subreddit = subreddit
        self.image_prefix = image_prefix
        self.valid_hosts = valid_hosts
        self.last_fetch_date = datetime.date.fromtimestamp(0)
        self.client = praw.Reddit(user_agent='opendank')

        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.title('opendank')
        self.window.update()
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.panel = tk.Label(self.window)
        self.panel.pack(side = 'bottom', fill = 'both', expand = 'yes')

    def store_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in response.iter_content(2**16):
                    image.write(chunk)
            return True
        return False

    def fetch_images(self):
        self.images = []

        hot_submissions = self.client.get_subreddit(self.subreddit).get_hot(limit=self.max_items)
        current_image = 0

        sys.stdout.write('Fetching images: [')
        for submission in hot_submissions:
            if any(host in submission.url for host in self.valid_hosts):
                image_path = self.image_prefix + str(current_image)
                sys.stdout.write('-')
                sys.stdout.flush()
                if self.store_image(submission.url, image_path):
                    self.images.append(image_path)
                    current_image += 1
        print(']')

    def clear_cache(self):
        for filename in glob.glob(self.image_prefix + '*'):
            os.remove(filename)

    def display_active(self):
        photo = Image.open(self.images[self.active])
        target_size = (self.width, self.height)
        photo.thumbnail(target_size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(photo)
        self.panel.configure(image = image)
        self.panel.image = image

    def update(self):
        current_date = datetime.date.today()
        if current_date.day != self.last_fetch_date.day:
            self.clear_cache()
            self.fetch_images()
            self.last_fetch_date = current_date
        self.active = (self.active + 1) % len(self.images)
        self.display_active()
        self.window.after(self.update_interval, self.update)

    def destroy(self, event):
        self.window.destroy()
        self.clear_cache()
        sys.exit(0)

    def start(self):
        self.update()
        self.window.bind("<Escape>", self.destroy)
        self.window.mainloop()

def main():
    diashow = ImageDiashow()
    diashow.start()

if __name__ == "__main__":
    main()
