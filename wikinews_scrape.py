import argparse

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys


def scrape_wikinews(query):
    # Define the search query in the URL
    url = f'https://en.wikinews.org/w/index.php?title=Special:Search&limit=20&offset=0&ns0=1&search={query}'

    # Send a request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the news articles in the search results
    articles = soup.find_all("li", attrs="mw-search-result")

    # Create an empty list to store the data of the articles
    data = []

    # Extract the data of the articles and add them to the list
    for index, article in enumerate(articles):
        title = article.find("div",attrs="mw-search-result-heading").text
        date = article.find("div", attrs="mw-search-result-data").text
        source = 'https://en.m.wikinews.org'+article.find("a")['href']
        summary = article.find("div", attrs="searchresult").text
        data.append((index + 1, title, date, source, summary))

    # Create a pandas dataframe with the article data
    df = pd.DataFrame(data, columns=['No', 'Judul', 'Tanggal','Source', 'Isi Berita' ])

    # Export the dataframe to an Excel file
    filename = f'{query.replace(" ", "_")}_news.xlsx'
    df.to_excel(filename, index=False)
    print(f'Search results for "{query}" have been saved to {filename} file.')

if len(sys.argv) > 1:
    query = ' '.join(sys.argv[1:])
    scrape_wikinews(query)
else:
    print('Please provide a search query as a command line argument.')
