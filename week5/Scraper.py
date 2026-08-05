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
    """ """

def clean_book(raw_book):
    """ """ 

def scrape_all_pages(base_url, num_pages):
    """"""
    
def save_to_json(records,filename):
    """ """
    
if __name__ == "__main__":
        
    url = "https://books.toscrape.com/"
    headers = {"User-Agent": "RankAI-Week5-Scraper"}

    html=fetch_page(url,headers)
    soup = parse_html(html)
    books = soup.find_all("article", class_="product_pod")

    print("NUmber of books found on this page:",len(books))