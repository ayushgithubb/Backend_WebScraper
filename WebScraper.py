import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
from datetime import date

def scrape_articles(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the articles on the page
    articles = soup.find_all('article', class_='c-compact-river__entry')

    # Initialize empty list to store article details
    article_details = []

    # Loop through each article and extract the required details
    for article in articles:
        # Extract the headline and the link to the article
        headline_element = article.find('h2', class_='c-entry-box--compact__title')
        headline = headline_element.text.strip()
        link = headline_element.a['href']

        # Extract the author and the date of the article
        byline_element = article.find('div', class_='c-byline')
        if byline_element:
            author = byline_element.find('a', class_='c-byline__author-name').text.strip()
            date_published = byline_element.find('time', class_='c-byline__item').text.strip()
        else:
            author = None
            date_published = None

        # Add the article details to the list
        article_details.append((link, headline, author, date_published))

    return article_details

def save_to_csv(article_details):
    # Generate the filename with the current date
    today = date.today().strftime('%d%m%Y')
    filename = f"{today}_verge.csv"

    # Write the article details to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'URL', 'headline', 'author', 'date'])

        for i, (link, headline, author, date_published) in enumerate(article_details):
            writer.writerow([i+1, link, headline, author, date_published])

    print(f"CSV file '{filename}' saved successfully")

def save_to_database(article_details):
    # Connect to the SQLite database
    conn = sqlite3.connect('articles.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create the articles table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles 
                    (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date_published TEXT)''')

    # Insert the article details into the table
    for i, (link, headline, author, date_published) in enumerate(article_details):
        cursor.execute('INSERT OR IGNORE INTO articles (id, url, headline, author, date_published) VALUES (?, ?, ?, ?, ?)',
                       (i+1, link, headline, author, date_published))

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

    print("Articles saved to database successfully")

if __name__ == '__main__':
    # URL of the website to scrape
    url = 'https://www.theverge.com/'

    # Scrape the articles
    article_details = scrape_articles(url)

    # Save the articles to CSV
    save_to_csv(article_details)

    # Save the articles to the database
    save_to_database(article_details)
