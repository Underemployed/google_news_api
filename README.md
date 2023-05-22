<h1>Google News Sentiment Analysis</h1>

<p>This project scrapes news articles related to the Indian stock market from Google News, performs sentiment analysis on the article titles and descriptions using VADER (Valence Aware Dictionary and Sentiment Reasoner), and saves the analyzed data to an Excel file.</p>

<h2>Installation</h2>

<p>Clone the repository:</p>

<pre>
<code>git clone 'https://github.com/Underemployed/google_news_sentiment_analysis.git'</code>
</pre>

<p>Install the required dependencies:</p>

<pre>
<code>pip install -r requirements.txt</code>
</pre>

<p>Run the <code>google_news.py</code> script to scrape news articles and save them to a CSV file named <code>articles.csv</code>.</p>

<p>Run the <code>sentiment.py</code> script to perform sentiment analysis on the articles in <code>articles.csv</code> using VADER and save the analyzed data to an Excel file named <code>sentiment_analysis.xlsx</code>.</p>

<h2>Dependencies</h2>

<p>The following libraries are used in this project:</p>

<ul>
  <li>urllib.request: For sending HTTP requests and retrieving webpage content.</li>
  <li>bs4 (BeautifulSoup): For parsing HTML and extracting data from webpages.</li>
  <li>requests: For making HTTP requests.</li>
  <li>newspaper: For article extraction and natural language processing.</li>
  <li>time: For time-related functions.</li>
  <li>csv: For reading and writing CSV files.</li>
  <li>pandas: For data manipulation and analysis.</li>
  <li>vaderSentiment: For sentiment analysis using VADER.</li>
</ul>
