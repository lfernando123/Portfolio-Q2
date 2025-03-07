import requests
from bs4 import BeautifulSoup
import pymysql

def scrape_and_load_to_rds():
    # Web scraping
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = [book.h3.a["title"] for book in soup.find_all("article", class_="product_pod")]
    prices = [book.find("p", class_="price_color").text.strip().replace("£", "") for book in soup.find_all("article", class_="product_pod")]

    # RDS MySQL connection details
    host = "database-1.cvaim2ssqz52.ap-south-1.rds.amazonaws.com"  # Replace with your endpoint
    port = 3306
    user = "admin"  # Replace with your master username
    password = "m7gYSSJdL0Vk0bW"  # Replace with your master password
    database = "dbBOOKS"  # Replace with your database name

    # Connect to MySQL **without specifying a database first**
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.commit()
    
    # Now, connect to the database
    conn.select_db(database)

    # Create a table (if it doesn't exist)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Title VARCHAR(255),
        Price FLOAT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Insert scraped data into the table
    for title, price in zip(titles, prices):
        insert_query = "INSERT INTO Books (Title, Price) VALUES (%s, %s)"
        cursor.execute(insert_query, (title, float(price)))
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
    print("Data scraped and loaded into RDS MySQL.")

if __name__ == "__main__":
    scrape_and_load_to_rds()
# 