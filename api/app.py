import tldextract
from flask import Flask, jsonify, request
from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import newspaper
from flask_cors import CORS
import nltk
from concurrent.futures import ThreadPoolExecutor
import feedparser


nltk.download('punkt')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://underemployed.github.io"}})  # Allow GitHub as an origin
class ArticleScraper:
    def __init__(self, query, max_retries=3):
        self.query = query
        self.max_retries = max_retries
        self.query_encoded = quote(query)
        self.articles_data = []
        self.blacklist = set()

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
                retries += 1
                continue
        domain = tldextract.extract(url).domain  # Extract the domain from the URL
        print(f"Adding {domain} to the blacklist due to repeated failures.")
        self.add_to_blacklist(domain)
        return None

    async def fetch_articles(self):
        query_encoded = quote(self.query)
        feed_url = f"https://news.google.co.in/rss/search?q={query_encoded}&sort=date&num=100"
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            summary = entry.summary
            publish_time = entry.published

            data = {
            "title": title,
            "publish_time": publish_time,
            "summary": summary,
            "source": link
            }

            print(title)
            self.articles_data.append(data)


    def get_urls(self, webpage):
        soup = BeautifulSoup(webpage, 'lxml')
        url_tags = soup.find_all('a')
        for tag in url_tags:
            url = tag.get('href', '')
            if '/url?q=' in url:
                modified_url = url.split('/url?q=')[1].split('&sa=')[0]
                yield modified_url

    def parse_url(self, url):
        if 'google' in url.lower():
            print(f"Skipping blacklisted domain: {url}")
            domain = tldextract.extract(url).domain  # Extract the domain from the URL
            self.add_to_blacklist(domain.lower())
            return None

        article = self.download_article_with_retry(url)
        if article is None:
            print(f"Skipping article: {url}")
            return None

        title = article.title
        if 'you a robot?' in title.lower():
            return None
        summary = article.summary
        source = url
        publish_time = article.publish_date.strftime("%Y-%m-%d %H:%M:%S") if article.publish_date else ""

        if len(summary.split()) < 30:
            return None

        data = {
            "title": title,
            "publish_time": publish_time,
            "summary": summary,
            "source": source
        }
        print(title)
        return data

    def add_to_blacklist(self, domain):
        print(f"Adding {domain} to the blacklist")
        self.blacklist.add(domain)

@app.route('/api/articles', methods=['GET'])
async def scrape_articles():
    query = request.args.get('query', 'indian stock')
    scraper = ArticleScraper(query)
    await scraper.fetch_articles()
    print("Completed")

    # Print blacklisted websites
    print("Blacklisted Websites:", '\n'.join(scraper.blacklist))

    return jsonify({"articles": scraper.articles_data})

if __name__ == '__main__':
    app.run(debug=True)
