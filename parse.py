# import requests
# from bs4 import BeautifulSoup
# import json
#
# result = requests.get('https://dev.to/api/articles?top=50')
# src = result.content
#
# y = json.loads(result)
#
# # soup = BeautifulSoup(src, 'lxml')
# #
# # urls = []
# # for h2_tag in soup.find_all('h2'):
# #     a_tag = h2_tag.find('a')
# #     urls.append(a_tag)
#
# print(y)