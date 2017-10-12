#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import urllib
import re

BASE_URL = 'http://nlp.cs.illinois.edu/HockenmaierGroup/8k-pictures.html'
OUTPUT_DIR = 'imgs'


def get_image(url):
    pass


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for image_url, image_name in get_image(BASE_URL):
        urllib.request.urlretrieve(image_url,
                                   os.path.join(OUTPUT_DIR, image_name))


if __name__ == '__main__':
    main()
