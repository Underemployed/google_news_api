import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

link = "https://www.google.co.in/search?q=indian+stock&num=100&gl=IN&tbs=sbd:1,qdr:d&tbm=nws&source=lnt&num=100&gl=IN"
req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

filename = "articles.csv"
header = ["Title", "Time", "Description", "Source"]

with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    soup = BeautifulSoup(webpage, 'lxml')
    main_div = soup.body.select_one('div#main', class_="main")
    main_div_str = str(main_div)  # Convert main_div to a string
    f1_elements = re.findall(r'<a class="f1".*?</a>', main_div_str, re.DOTALL)
    for element in f1_elements:
        print(element)
