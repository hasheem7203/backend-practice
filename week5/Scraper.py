import requests
from bs4 import BeautifulSoup
import time
import json


def fetch_page(url,header):
    response = requests.get(url, headers=header)
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html,"html.parser")
    return soup

def extract_book(article):
    title = article.h3.a["title"]
    price = article.find("p",class_ = "price_color").text
    rating_class=article.find("p",class_ = "star-rating")["class"]
    stock = article.find("p",class_ = "instock availability").text
    
    return{
        "title":title,
        "price":price,
        "rating_class":rating_class,
        "stock":stock
    }
    
    
def clean_book(raw_book):
    
    price_text = raw_book["price"].replace("Â", "").replace("£", "")
    price = float(price_text)

    rating_word = raw_book["rating_class"][1]  # second item in the list
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_map.get(rating_word, 0)  # 0 if word not found, just in case

    stock = raw_book["stock"].strip()

    return {
        "title": raw_book["title"],
        "price": price,
        "rating": rating,
        "stock": stock
    }
    
def scrape_all_pages(base_url, num_pages):
    all_books = []
    header = {"User-Agent": "RankAI-Week5-Scraper"}
    for page_num in range(1, num_pages + 1):
        url = base_url.format(page_num)
        print(f"Scraping Page {page_num}: {url}")
        html = fetch_page(url,header)
        soup=   parse_html(html)
        books= soup.find_all("article",class_ = "product_pod")
        
        for book in books:
            raw_book = extract_book(book)
            clean=clean_book(raw_book)
            all_books.append(clean)
        
        time.sleep(1)
    return all_books
    
def save_to_json(records,filename):
    """ """
    
if __name__ == "__main__":
        
    url = "https://books.toscrape.com/catalogue/page-{}.html"

    all_books = scrape_all_pages(url,10)
    print(f"Total books scraped: {len(all_books)}")
    print("Sample record:", all_books[0])
    
    