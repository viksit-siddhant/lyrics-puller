import requests
from bs4 import BeautifulSoup
from unicodedata import normalize

with open('access_token','r') as f:
    access_token = f.read()

def get_search(search_term):

    search = requests.get(f'https://api.genius.com/search?q={search_term}',headers = {'Authorization':f'Bearer {access_token}'})

    search_hits = search.json()['response']['hits']
    urls = []
    titles = []
    for hit in search_hits:
        result = hit['result']
        titles.append(normalize('NFKD',result['full_title']))
        urls.append(result['url'])
    return titles,urls

def parse_lyrics(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    text = soup.find('div',class_="lyrics").get_text()
    return text.strip()

