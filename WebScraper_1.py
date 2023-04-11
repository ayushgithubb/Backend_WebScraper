## THE CODE IS UPDATED TO CATCH NEFARIOUS BUGS IN THE CODE ##

import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import logging
import datetime

# This sets up logging to write messages to a file named Webscraper.log. The logging level is set to DEBUG, and the message format is specified to include the timestamp and log level.
logging.basicConfig(filename='WebScraper.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')


def scrape_articles(url):
    logging.info('Starting to read articles...')

    
     # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f'Failed to fetch articles from {url}, status code: {response.status_code}')
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the articles on the page
    articles = soup.find_all('article', class_='c-entry-box--compact__title')

    # Initialize empty list to store article details
    article_details = []
   
    for article in articles:
        try:
            headline = article.find('h2', class_='c-entry-box--compact__title').text.strip()
            link = article.find('a')['href']
            author = article.find('span', class_='c-byline__item').text.strip()
            date = article.find('time')['datetime']


            article_details.append((link, headline, author, date))
        except Exception as e:
            logging.warning(f'Failed to parse article: {str(e)}')

    logging.info(f'Read {len(data)} articles')
    return article_details


def save_to_csv(data):
    logging.info('Saving data to CSV...')

    # Generate the filename with the current date
    filename = datetime.datetime.now().strftime("%d%m%Y") + '_verge.csv'

    # Write the article details to a CSV file
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'URL', 'headline', 'author', 'date'])

        for idx, article in enumerate(data):
            writer.writerow([idx+1, *article])

    logging.info(f'Data saved to {filename}')


def save_to_database(data, db_name):
    logging.info('Saving data to database...')

    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)

    # Create a cursor object
    c = conn.cursor()

    # Create the articles table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY,
                  url TEXT,
                  headline TEXT,
                  author TEXT,
                  date TEXT)''')

    # Insert the article details into the table
    for i, article in enumerate(data):
        try:
            c.execute('INSERT INTO articles VALUES (?, ?, ?, ?, ?)',
                      (i+1, article[0], article[1], article[2], article[3]))
        except Exception as e:
            logging.warning(f'Failed to insert article: {str(e)}')

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

    logging.info(f'Data saved to {db_name}')


if __name__ == '__main__':
    
    # extract the url
    url = 'https://www.theverge.com/'

    # store data in a list
    data=[]
    data = scrape_articles(url)

    if data:
        save_to_csv(data)
        save_to_database(data, 'verge.db')

    else:
        logging.warning('No data to save.')
