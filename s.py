from pprint import pprint
from typing import List, Dict

from bs4 import BeautifulSoup
import requests

# if __name__ == '__main__':

#    result = requests.get('https://dev.to/api/articles?top=50')

#    username_json = result.json()

#    sabaka = username_json[0].get('user').get('username')

#    kekw = requests.get(f'https://dev.to/{sabaka}')

#    soup = BeautifulSoup(kekw.text, 'lxml')

#    print(soup)


if __name__ == "__main__":
    a = requests.get("https://dev.to/balvinder294")

    soup = BeautifulSoup(a.text, "lxml")

    meta = soup.find_all("div", {"class": ["key", "value"]})
    keys: List[str] = []
    values: List[str] = []
    for tag in meta:
        if tag.get("class") == ["key"]:
            keys.append(tag.text.strip())
        elif tag.get("class") == ["value"]:
            values.append(tag.text.strip())

    developer_info: Dict[str, str] = dict(zip(keys, values))

    pprint(developer_info)
