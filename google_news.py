from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import newspaper
import time
    
# headline_pattern = re.compile(r'<h3[^>]*>(.*?)<\/h3>', re.IGNORECASE) couldnt get full heading

link = "https://www.google.co.in/search?q=indian+stock&num=100&gl=IN&tbs=sbd:1,qdr:d&tbm=nws&source=lnt&num=100&gl=IN"
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
with requests.Session() as c:
    soup = BeautifulSoup(webpage, 'lxml')
    url_tags = soup.find_all('a')
    for tag in url_tags:
        url = tag['href']
        if '/url?q=' in url and not ('google' in url) and not ('equitymaster' in url) and not ('youtube' in url):
            modified_url = url.split('/url?q=')[1].split('&sa=')[0]
            # Extract title and summary using newspaper3k
            article = newspaper.Article(modified_url) 
            article.download()
            time.sleep(5)
            try:
                article.parse()
                article.nlp()
                title = article.title
                summary = article.summary
                print("<="+"="*100+"=>")
                print(f"URL: {modified_url}")
                print(f"Title: {title}")
                print(f"Summary: {summary}")
                print()
            except Exception as e:
                continue
