#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import urllib
import re
from pit import Pit
from xml.etree import ElementTree

BASE_URL = 'http://nlp.cs.illinois.edu/HockenmaierGroup/8k-pictures.html'
OUTPUT_DIR = 'imgs'
FLICKR_REST_EP_URL = 'https://api.flickr.com/services/rest/'
FLICKR_PHOTOS_METHOD = 'flickr.photos.getSizes'


def get_image_original_size(xml_root):
    for elems in xml_root:
        # use a larger size
        elem = elems[-1]
        image_url = elem.get('source')
        p = urllib.parse.urlparse(image_url)
        image_name = p.path.split('/')[-1]
        return image_url, image_name


def get_image(url, config):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    links = soup.find_all('a')

    for link in links:
        if re.match(r'http', link.text):
            p = urllib.parse.urlparse(link.text)
            photo_id = p.path.split('/')[-2]
            photo_req = requests.get(FLICKR_REST_EP_URL, {
                'api_key': config['API_KEY'],
                'method': FLICKR_PHOTOS_METHOD,
                'photo_id': photo_id
            })
            root = ElementTree.fromstring(photo_req.text)
            if root.get('stat') == 'fail':
                continue
            image_url, image_name = get_image_original_size(root)
            yield image_url, image_name


def main():
    config = Pit.get('flickr.com')

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for image_url, image_name in get_image(BASE_URL, config):
        urllib.request.urlretrieve(image_url,
                                   os.path.join(OUTPUT_DIR, image_name))
        print('Got {}.'.format(os.path.join(OUTPUT_DIR, image_name)))


if __name__ == '__main__':
    main()
