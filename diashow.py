"""Module diashow provides functionality for displaying images from the WWW."""
import sys
import os
import glob
import datetime
import Tkinter as tk
import requests
from PIL import ImageTk, Image


class Diashow(object):
    """Class Diashow downloads and displays images."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
            self,
            image_prefix="image",
            update_interval=10000,
            quit_key="<Escape>"):
        self.quit_key = quit_key
        self.update_interval = update_interval
        self.active = 0
        self.sources = []
        self.image_prefix = image_prefix
        self.last_fetch_date = datetime.date.fromtimestamp(0)
        self.images = []
        self.store_mode = "wb"

        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.title("opendank")
        self.window.update()
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.panel = tk.Label(self.window)
        self.panel.pack(side="bottom", fill="both", expand="yes")

    def store_image(self, url, filename):
        """Downloads an image from a specific url and stores it."""
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, self.store_mode) as image:
                for chunk in response.iter_content(2**16):
                    image.write(chunk)
            return True
        return False

    def add_source(self, source_class):
        """Add image source to diashow."""
        self.sources.append(source_class)

    def fetch_images(self):
        """Fetch images from sources."""
        self.images = []
        image_urls = []
        for source in self.sources:
            image_urls += source.fetch_images()
        current_image = 0

        sys.stdout.write("Fetching images: [")

        for url in image_urls:
            image_path = self.image_prefix + str(current_image)
            sys.stdout.write("-")
            sys.stdout.flush()
            if self.store_image(url, image_path):
                self.images.append(image_path)
                current_image += 1
        print "]"

    def clear_cache(self):
        """Remove stored image artifacts."""
        for filename in glob.glob(self.image_prefix + "*"):
            os.remove(filename)

    def display_active(self):
        """Update screen to show active image."""
        photo = Image.open(self.images[self.active])
        target_size = (self.width, self.height)
        photo.thumbnail(target_size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(photo)
        self.panel.configure(image=image)
        self.panel.image = image

    def update(self):
        """Update the screen, images and sources."""
        current_date = datetime.date.today()
        if current_date.day != self.last_fetch_date.day:
            self.clear_cache()
            self.fetch_images()
            self.last_fetch_date = current_date
        self.active = (self.active + 1) % len(self.images)
        self.display_active()
        self.window.after(self.update_interval, self.update)

    def destroy(self, _):
        """Destroy the diashow window and free all resources."""
        self.window.destroy()
        self.clear_cache()
        sys.exit(0)

    def start(self):
        """Start the diashow."""
        self.update()
        self.window.bind(self.quit_key, self.destroy)
        self.window.mainloop()
