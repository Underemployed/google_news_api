from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import re

link = "https://www.google.com/search?q=indian+stock&client=firefox-b-d&tbas=0&tbs=sbd:1,qdr:d&tbm=nws&sxsrf=APwXEdda0VaUcKYj_npOoApwunxhZNK77g:1684653847046&source=lnt&sa=X&ved=2ahUKEwjHjv3Q8IX_AhUtUWwGHaRCDQAQpwV6BAgCEBY&biw=1600&bih=814&dpr=1"
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

headline_pattern = re.compile(r'<h3[^>]*>(.*?)<\/h3>', re.IGNORECASE)

data = {}

with requests.Session() as c:
    soup = BeautifulSoup(webpage, 'lxml')
    headline_tags = soup.find_all(lambda tag: tag.name == 'h3' and headline_pattern.match(str(tag)))
    for tag in headline_tags:
        headline = tag.text
        
        url_tag = tag.find_next('a')
        url = url_tag['href']
        if '/url?q=' in url and not ('google' in url):
            modified_url = url.split('/url?q=')[1].split('&amp;sa=U&amp;ved=')[0]
            
            data[headline] = modified_url

for headline, url in data.items():
    print(f"Headline: {headline}")
    print(f"URL: {url}")
    print()
