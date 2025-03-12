import requests
from bs4 import BeautifulSoup
import pymysql

def scrape_and_load_to_rds():
    # Initialize lists to store data
    titles = []
    prices = []
    ratings = []
    availabilities = []
    categories = []

    # Loop through the first 5 pages (for simplicity)
    for page in range(1, 50):
        url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract book details
        for book in soup.find_all("article", class_="product_pod"):
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            rating = book.p["class"][1]  # Extract rating (e.g., "Three")
            availability = book.find("p", class_="instock availability").text.strip()

            # Navigate to the book's detail page to get category and description
            book_url = "http://books.toscrape.com/catalogue/" + book.h3.a["href"].replace("../../../", "")
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.text, "html.parser")
            category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()

            cleaned_price = price.replace("Â£", "").replace("Ã", "").strip()

            # Append data to lists
            titles.append(title)
            prices.append(cleaned_price)
            ratings.append(rating)
            availabilities.append(availability)
            categories.append(category)

    # RDS MySQL connection details
    host = "database-1.cvaim2ssqz52.ap-south-1.rds.amazonaws.com"
    port = 3306
    user = "admin"
    password = "m7gYSSJdL0Vk0bW"
    database = "dbBOOKS"

    # Connect to MySQL
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # # Create database if it doesn't exist
    # cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    # conn.commit()
    
    # connect to the database
    conn.select_db(database)

    drop_table_query = "DROP TABLE IF EXISTS tBooks;"
    cursor.execute(drop_table_query)
    conn.commit()

    # Create a table (if it doesn't exist)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tBooks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Title VARCHAR(255),
        Price FLOAT,
        Rating VARCHAR(10),
        Availability VARCHAR(20),
        Category VARCHAR(100)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Insert scraped data into the table
    for title, price, rating, availability, category in zip(titles, prices, ratings, availabilities, categories):
        insert_query = "INSERT INTO tBooks (Title, Price, Rating, Availability, Category) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(insert_query, (title, float(price), rating, availability, category))
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
    print("Data scraped and loaded into RDS MySQL.")

if __name__ == "__main__":
    scrape_and_load_to_rds()
# 