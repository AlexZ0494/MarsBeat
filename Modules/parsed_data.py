from dataclasses import dataclass
import requests


@dataclass
class Album:
    title: str = None
    img: str = None
    url: str = None

    def __post_init__(self):
        # add an insert to the table
        # or delete this file altogether
        self.url = self.url.replace('https://rur.hitmotop.com//', 'https://rur.hitmotop.com/')
        if requests.get(self.url).status_code == 200:
            if self.img:
                self.img = "https:" + self.img.replace("background-image: url('", "").replace("')", "")
                try:
                    requests.get(self.img)
                except requests.exceptions.InvalidURL:
                    self.img = self.img.replace("https:/", "https://rur.hitmotop.com/")
                if requests.get(self.img).status_code == 404:
                    self.img = 'https://cdn-img.readytotrip.com/t/1024x768/content/ea/5a/ea5a73506007c96cece08c6dfcba490291839de1.jpeg'
            self.img = requests.get(self.img).content
        else:
            self.url = None


@dataclass
class Track:
    title: str = None
    author: str = None
    img: str = None
    url: str = None
