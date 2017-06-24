from bs4 import BeautifulSoup
import requests
import re
import os
#import cookielib
from http.cookiejar import CookieJar
import json

def get_soup(url,headers):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content)
    #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


query = "nike air max blue"# you can change the query for the image  here
queries = ["adidas gazelle black",
        "converse all star black high tops",
        "nike air force high white",
        "nike air force low white",
        "nike air jordan 1 black red",
        "nike roshe one gym red",
        "stan smith white green",
        "timberland earthkeepers",
        "yeezy 2 red",
        "yeezy boost zebra"]

for query in queries:
    image_type="ActiOn"
    query= query.split()
    dirname = '_'.join(query)
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    print(url)
    #add the directory for your image here
    DIR="Pictures"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)


    ActualImages=[]# contains the link for Large original images, type of  image
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        ActualImages.append((link,Type))

    print("there are total" , len(ActualImages),"images")

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    DIR = os.path.join(DIR, dirname.split()[0])

    if not os.path.exists(DIR):
        os.mkdir(DIR)
    for i , (img , Type) in enumerate( ActualImages):
        try:
            r = requests.get(img, headers=header)
            raw_img = r.content

            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
            print(cntr)
            if len(Type)==0:
                f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
            else :
                f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : "+img)
            print(e)
