import csv
from bs4 import BeautifulSoup
import requests


urls = ["https://www.jumia.com.tn/smartphones/",
        "https://www.jumia.com.tn/smartphones/?page=2#catalog-listing",
            "https://www.jumia.com.tn/smartphones/?page=3#catalog-listing",
            "https://www.jumia.com.tn/smartphones/?page=4#catalog-listing",
            "https://www.jumia.com.tn/smartphones/?page=5#catalog-listing",
            "https://www.jumia.com.tn/smartphones/?page=6#catalog-listing",
            "https://www.jumia.com.tn/smartphones/?page=7#catalog-listing"]
all_urls = []


with open('products.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Price', 'Image', 'Link'])
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        products = soup.find_all('article', class_='prd _fb col c-prd')
        all_urls.extend(products)
        for product in products:
            brand = product.find("a", class_='core')["data-brand"]
            name = product.find("h3", class_='name').text
            price = product.find("div", class_='prc').text
            price = float(price.replace(",","").rstrip("TND"))
            image = product.find("img", class_='img')["data-src"]
            link = product.find("a", class_="core")['href']
            link = "https://www.jumia.com.tn/smartphones/" + link 
            writer.writerow([brand, name, price, image, link])