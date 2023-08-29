import requests
from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import newspaper
import json
import os
from flask import Flask, jsonify,request
from flask_cors import CORS
import nltk
nltk.download('punkt')
app = Flask(__name__)
CORS(app)
class ArticleScraper:
    def __init__(self, query, max_retries=3, blacklist_file="blacklist.txt", data_file="articles.json"):
        self.query = query
        self.max_retries = max_retries
        self.blacklist_file = blacklist_file
        self.data_file = data_file
        self.query_encoded = quote(query)
        self.articles_data = []

    def load_blacklist(self):
        try:
            with open(self.blacklist_file, 'r') as file:
                return set(file.read().splitlines())
        except FileNotFoundError:
            return set()

    def download_article_with_retry(self, url):
        retries = 0
        while retries < self.max_retries:
            try:
                article = newspaper.Article(url)
                article.download()
                article.parse()
                article.nlp()
                return article
            except Exception as e:
                print(f"Error downloading article from {url}: {str(e)}")
                print(f"Retrying in 5 seconds...")
                retries += 1
                continue
        return None

    def fetch_articles(self):
        link = f"https://www.google.co.in/search?q={self.query_encoded}&num=1&gl=IN&tbs=sbd:1,qdr:d&tbm=nws&source=lnt&num=100&gl=IN"
        print(link)
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        blacklist = self.load_blacklist()

        with requests.Session() as c:
            soup = BeautifulSoup(webpage, 'lxml')
            url_tags = soup.find_all('a')
            for tag in url_tags:
                url = tag.get('href', '')
                if '/url?q=' in url:
                    modified_url = url.split('/url?q=')[1].split('&sa=')[0]
                    domain = modified_url.split('/')[2].lower()
                    if domain in blacklist:
                        print(f"Skipping blacklisted domain: {domain}")
                        continue

                    article = self.download_article_with_retry(modified_url)
                    if article is None:
                        print(f"Skipping article: {modified_url}")
                        blacklist.add(domain)
                        continue

                    title = article.title
                    if 'you a robot?' in title.lower():
                        continue
                    summary = article.summary
                    source = modified_url
                    publish_time = article.publish_date.strftime("%Y-%m-%d %H:%M:%S") if article.publish_date else ""

                    if len(summary.split()) < 30:
                        continue
                    
                    data = {
                        "title": title,
                        "publish_time": publish_time,
                        "summary": summary,
                        "source": source
                    }
                    self.articles_data.append(data)

        with open(self.blacklist_file, 'w') as file:
            file.write('\n'.join(blacklist))

        with open(self.data_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.articles_data, json_file, ensure_ascii=False, indent=4)


@app.route('/api/articles', methods=['GET'])
def scrape_articles():
    query = request.args.get('query', 'indian stock')  # Default to "indian stock" if query parameter is not provided
    scraper = ArticleScraper(query)
    scraper.fetch_articles()
    with open(scraper.data_file, 'r', encoding='utf-8') as json_file:
        articles_data = json.load(json_file)
    return jsonify({"articles": articles_data})
if __name__ == '__main__':
    app.run(debug=True)
