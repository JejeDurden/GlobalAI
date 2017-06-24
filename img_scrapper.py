import urllib2
from bs4 import BeautifulSoup

def find_all_img(url):
    test_url = url
    request = urllib2.Request(test_url)
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page,"html.parser")
    links = soup.findAll('img')
    links = [tag['src'] for tag in links if ".jpg" in tag['src'].lower()]
    return links
