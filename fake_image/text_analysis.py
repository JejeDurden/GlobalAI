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
 




def search():
    if request.headers['Content-Type'] != 'application/json':
        return "Requests must be in JSON format. Please make sure the header is 'application/json' and the JSON is valid."

    client_json = json.dumps(request.json)
    client_data = json.loads(client_json)
    code = doImageSearch(client_data['image_url'])
    return parseResults(code)

def doImageSearch(image_url):
    """Perform the image search and return the HTML page response."""

    if python3:
        returned_code = bytesIOModule.BytesIO()
    else:
        returned_code = StringIO()
    full_url = SEARCH_URL + image_url

    if app.debug:
        print('POST: ' + full_url)

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

    return json.dumps(results)

def main():
    parser = argparse.ArgumentParser(description='Meta Reverse Image Search API')
    parser.add_argument('-p', '--pef main():
    parser = argparse.ArgumentParser(description='Meta Reverse Image Search API')
    parser.add_argument('-p', '--port', type=int, default=5000, help='port number')
    parser.add_argument('--debug', action='store_true', help='enable debug mode')
    args = parser.parse_args()

    if args.debug:
        app.debug = True

    app.run(host='0.0.0.0', port=args.port)
ort', type=int, default=5000, help='port number')
    parser.add_argument('--debug', action='store_true', help='enable debug mode')
    args = parser.parse_args()

    if args.debug:
        app.debug = True

    app.run(host='0.0.0.0', port=args.port)

