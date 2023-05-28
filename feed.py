import feedparser
from bs4 import BeautifulSoup
import newspaper
from newspaper import Config
import csv
search_query = input("Enter search query\n>").replace(" ","+")

url = f"https://news.google.co.in/rss/search?q={search_query}&sort=date&num=1000"
header = ["Title", "Time", "Description", "Source"]
feed = feedparser.parse(url)
config = Config()
config.request_timeout = 100
with open("article.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for entry in feed.entries:
        article = newspaper.Article(entry.link,config=config)
        article.download()
        try:
            article.parse()
            article.nlp()
            title = article.title
            summary = article.summary
            description_html = entry.description
            soup = BeautifulSoup(description_html, "html.parser")
            description_text = soup.get_text(separator=" ")
            source = entry.link
            publish_time = entry.published
            data = [title, publish_time, summary, source]
            writer.writerow(data)
            
            print("<=" + "=" * 100 + "=>")
            print(f"URL: {url}")
            print(f"Title: {title}")
            print(f"Publish Time: {publish_time}")
            print(f"Summary: {summary}")
            print()
        except Exception as e:
            print("Error processing article: ", e)
            continue

        

print("Data saved to file")
