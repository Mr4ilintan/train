from bs4 import BeautifulSoup
import requests

#if __name__ == '__main__':

#    result = requests.get('https://dev.to/api/articles?top=50')

#    username_json = result.json()

#    sabaka = username_json[0].get('user').get('username')

#    kekw = requests.get(f'https://dev.to/{sabaka}')

#    soup = BeautifulSoup(kekw.text, 'lxml')

#    print(soup)

a = requests.get('https://dev.to/balvinder294')

soup = BeautifulSoup(a.text, 'lxml')

meta = soup.find_all('div', {
    'class': ['key', 'value']
})



print(meta)

