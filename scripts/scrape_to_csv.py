import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize lists to store data
titles = []
prices = []
ratings = []
availabilities = []
categories = []
#descriptions = []
#image_urls = []

# Loop through the first 5 pages (for simplicity)
for page in range(1, 20):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract book details
    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        rating = book.p["class"][1]  # Extract rating (e.g., "Three")
        availability = book.find("p", class_="instock availability").text.strip()
        #image_url = "http://books.toscrape.com/" + book.img["src"].replace("../../", "")

        # Navigate to the book's detail page to get category and description
        book_url = "http://books.toscrape.com/catalogue/" + book.h3.a["href"].replace("../../../", "")
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, "html.parser")
        category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
        #description = book_soup.find("meta", attrs={"name": "description"})["content"].strip()

        # Append data to lists
        titles.append(title)
        prices.append(price)
        ratings.append(rating)
        availabilities.append(availability)
        categories.append(category)
        #descriptions.append(description)
        #image_urls.append(image_url)

# Create a DataFrame
data = {
    "Title": titles,
    "Price": prices,
    "Rating": ratings,
    "Availability": availabilities,
    "Category": categories,
    # "Description": descriptions,
    # "Image_URL": image_urls
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("books_data.csv", index=False)

# Display the DataFrame
print(df.head())