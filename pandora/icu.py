from bs4 import BeautifulSoup
import requests
from pprint import pprint as print

html = requests.get("https://github.com/996icu/996.ICU/blob/master/blacklist/README.md",
                    proxies={"https": "127.0.0.1:1080"}).text
# text = ''.join(BeautifulSoup(html,'html.parser').findAll(text=True))
# print(text)
soup = BeautifulSoup(html, 'lxml')
# print(soup.find(id='readme').article.find_all('table')[1].tbody.find_all('tr')[0].find_all('td')[0].text)
# res=[[k.text for k in j.find_all('td')] for j in [i for i in soup.find(id='readme').article.find_all('table')[1].tbody.find_all('tr')]]
res = [dict(zip(["city", "company", "exposure_time", "description"], [j.text for j in i.find_all('td')][:4])) for i in
       soup.find(id='readme').article.find_all('table')[1].tbody.find_all('tr')]
print(res)
