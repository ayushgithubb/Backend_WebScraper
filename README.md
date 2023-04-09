# Backend_WebScraper
I have written a Python code that scrapes article details from a website and saves them to both a CSV file and a SQLite database.
=======================================================================================================================================================================
The code uses the following libraries:
	requests: to send HTTP requests and get the HTML content of the web page.
	BeautifulSoup: to parse the HTML content and extract the article details.
	csv: to write the article details to a CSV file.
	sqlite3: to connect to a SQLite database and write the article details to a table.
	datetime: to get the current date and use it in the filename of the CSV file.

We have to install the first two libraries : requests and BeautifulSoup using the following command in terminal : 

$  py -m pip install requests
$  py -m pip install bs4
The other libraries are pre-defined.

The code defines three functions:
	scrape_articles(url): This function takes a URL as input and returns a list of tuples containing the article details. The function sends a GET request to the URL, parses the HTML content using BeautifulSoup, finds all the articles on the page, loops through each article, and extracts the headline, the link to the article, the author, and the date of the article. The function then appends these details as a tuple to the article_details list.

	save_to_csv(article_details): This function takes the list of article details as input and saves them to a CSV file. The function generates a filename using the current date, opens a file with that name in write mode, writes the header row and each article detail as a row in the file using the csv module. Finally, the function prints a message indicating the file was saved successfully.

	save_to_database(article_details): This function takes the list of article details as input and saves them to a SQLite database. The function connects to the database, creates a cursor object, creates a table called articles if it doesn't exist, and inserts each article detail into the table. The function then commits the changes to the database, closes the connection, and prints a message indicating the articles were saved successfully.

At the end of the code, the script checks if it is being run as the main program and then calls the scrape_articles(), save_to_csv(), and save_to_database() functions to scrape the articles, save them to a CSV file, and save them to a SQLite database.

Some more information about the code:

	In the save_to_csv() function, the current date is obtained using the date.today() method from the datetime module and formatted as a string in the '%d%m%Y' format, which is used to generate the filename for the CSV file. Then, the csv module is used to write the article details to a CSV file named ddmmyyyy_verge.csv. The csv.writer() method is used to create a writer object for the CSV file, and the writerow() method is used to write the header row and each row of article details to the CSV file.

	In the save_to_database() function, the sqlite3 module is used to create a connection to a SQLite database file named articles.db. A cursor object is created to interact with the database. If the articles table does not exist in the database, it is created with columns for id, url, headline, author, and date_published.


	For each article, the article details are inserted into the articles table using the cursor.execute() method with an SQL INSERT OR IGNORE statement. The id column is auto-incremented for each article using the i+1 value.

	 The changes to the database are committed using the conn.commit() method, and the database connection is closed using the conn.close() method.


	Finally, in the if __name__ == '__main__' block, the URL of the website to scrape is defined as url. The scrape_articles function is called to scrape the articles, and the article details are saved to both a CSV file and a SQLite database using the save_to_csv() and save_to_database() functions.


