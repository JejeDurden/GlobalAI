import urllib, cStringIO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
import pandas as pd
import urllib2
import scipy
import scipy.misc
from scipy import spatial as sp
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import re
from unidecode import unidecode


#--------------------------------#
import pycurl
import json
#from flask import Flask, url_for, json, request
python3 = False
try:
    from StringIO import StringIO
except ImportError:
    python3 = True
    import io as bytesIOModule
from bs4 import BeautifulSoup
if python3:
    import certifi
SEARCH_URL = 'https://www.google.com/searchbyimage?&image_url='

#--------------------------------#
#global var

request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    #"Connection": "keep-alive" 
    }

#--------------------------------#
def doImageSearch(image_url):
    """Perform the image search and return the HTML page response."""

    if python3:
        returned_code = bytesIOModule.BytesIO()
    else:
        returned_code = StringIO()
    full_url = SEARCH_URL + image_url


    conn = pycurl.Curl()
    if python3:
        conn.setopt(conn.CAINFO, certifi.where())
    conn.setopt(conn.URL, str(full_url))
    conn.setopt(conn.FOLLOWLOCATION, 1)
    conn.setopt(conn.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')
    conn.setopt(conn.WRITEFUNCTION, returned_code.write)
    conn.perform()
    conn.close()
    if python3:
        return returned_code.getvalue().decode('UTF-8')
    else:
        return returned_code.getvalue()
    
def parseResults(code):
    """Parse/Scrape the HTML code for the info we want."""

    soup = BeautifulSoup(code, 'html.parser')

    results = {
        'links': [],
        'descriptions': [],
        'titles': [],
        'similar_images': []
    }

    for div in soup.findAll('div', attrs={'class':'g'}):
        sLink = div.find('a')
        results['links'].append(sLink['href'])

    for desc in soup.findAll('span', attrs={'class':'st'}):
        results['descriptions'].append(desc.get_text())

    for title in soup.findAll('h3', attrs={'class':'r'}):
        results['titles'].append(title.get_text())

    for similar_image in soup.findAll('div', attrs={'rg_meta'}):
        tmp = json.loads(similar_image.get_text())
        img_url = tmp['ou']
        results['similar_images'].append(img_url)

    #return json.dumps(results)
    return results

def extract_reverse_url(dic):
    if dic:
        return dic['links']
    else:
        return
    
    
def dl_text(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    return texts

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', element):
        return False
    return True

def get_main_txt(visible_texts,idx=None):
    if idx:
        size = [len(x) for x in visible_texts]
        size_ = [x for x in size if x<max(size)]
        max_idx=max(size_)
        return visible_texts[size.index(max_idx)]
    else:
        size = [len(x) for x in visible_texts]
        max_idx=max(size)
        return visible_texts[size.index(max_idx)]


def find_all_img(url):
    test_url = url
    request = urllib2.Request(test_url)
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page,"html.parser")
    links = soup.findAll('img')
    links = [tag['src'] for tag in links if ".jpg" in tag['src'].lower()]
    return links

def get_biggest_imgs(links):
    keep=[]
    for element in links:
        file = cStringIO.StringIO(urllib.urlopen(element).read())
        img = Image.open(file)
        keep.append(img.size[0]*img.size[1])
    df = pd.DataFrame()
    df["url"]=links
    df["size"]=keep
    df = df.sort_values("size",ascending=False)
    return list(df["url"][0:3])

