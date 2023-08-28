from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import newspaper
import csv
    
link = "https://www.google.co.in/search?q=indian+stock&num=100&gl=IN&tbs=sbd:1,qdr:d&tbm=nws&source=lnt&num=100&gl=IN"
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

filename = "articles.csv"
header = ["Title", "Time", "Description", "Source"]

with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

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
                try:
                    article.parse()
                    article.nlp()
                    title = article.title
                    summary = article.summary
                    source = modified_url
                    publish_time = article.publish_date.strftime("%Y-%m-%d %H:%M:%S") if article.publish_date else ""

                    # Skip articles with description less than 30 words
                    if len(summary.split()) < 30:
                        continue

                    data = [title, publish_time, summary, source]
                    writer.writerow(data)

                    print("<=" + "=" * 100 + "=>")
                    print(f"URL: {modified_url}")
                    print(f"Title: {title}")
                    print(f"Publish Time: {publish_time}")
                    print(f"Summary: {summary}")
                    print()

                except Exception as e:
                    continue

print(f"Data saved to {filename}")
