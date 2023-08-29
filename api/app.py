import aiohttp
import asyncio
from flask import Flask, jsonify, request
from urllib.parse import quote
import newspaper
from newspaper import Config
from flask_cors import CORS
import nltk
import feedparser
import concurrent.futures

nltk.download('punkt')
config = Config()
config.request_timeout = 100
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://underemployed.github.io"}})  # Allow GitHub as an origin

class ArticleScraper:
    def __init__(self, query, max_retries=3):
        self.query = query
        self.max_retries = max_retries
        self.query_encoded = quote(query)
        self.articles_data = []

    async def download_article_with_retry(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    article = newspaper.Article(url, config=config)
                    article.set_html(content)
                    article.parse()
                    article.nlp()
                    return article
        except Exception as e:
            print(f"Error downloading article from {url}: {str(e)}")            
        return None

    async def fetch_article_data(self, session, entry):
        title = entry.title
        link = entry.link
        publish_time = entry.published

        # Fetch the article using aiohttp
        article = await self.download_article_with_retry(session, link)

        if article is None:
            return None

        # Get the title, summary, and article text

        data = {
            "title": entry.summary,
            "publish_time": publish_time,
            "summary": article.summary,
            "source": link,
        }
        self.articles_data.append(data)

    async def fetch_articles(self):
        query_encoded = quote(self.query)
        feed_url = f"https://news.google.co.in/rss/search?q={query_encoded}&sort=date&num=1"
        feed = feedparser.parse(feed_url)

        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_article_data(session, entry) for entry in feed.entries]
            await asyncio.gather(*tasks)

@app.route('/api/articles', methods=['GET'])
def scrape_articles():
    query = request.args.get('query', 'indian stock')
    scraper = ArticleScraper(query)
    asyncio.run(scraper.fetch_articles())
    print("Completed")

    return jsonify({"articles": scraper.articles_data})

if __name__ == '__main__':
    app.run(debug=True)
