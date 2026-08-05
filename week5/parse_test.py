import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
headers = {"User-Agent": "RankAI-Week5-Scraper"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text,"html.parser")

books = soup.find_all("article", class_="product_pod")

print("NUmber of books found on this page:",len(books))
print()
print("First book's raw html")
print(books[0])