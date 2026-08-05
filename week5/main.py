import requests
url = "https://books.toscrape.com"

headers = {
    "User-Agent": "FlyRankAI-Week5-Scraper Project"
}

response = requests.get(url,headers=headers)

print ("Status Code: ",response.status_code)
print("First 500 characters of html")
print(response.text[:500])