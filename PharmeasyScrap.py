
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup


#create class
class PriceScraper:
    def __init__(self):
        pass
    def scrape_price(self,url):
        
    # url = request.json.get('url')

        if not url:
            return jsonify({'error': 'URL not provided.'}), 400
        fullurl="https://pharmeasy.in/search/all?name="+url
        response = requests.get(fullurl)
        soup = BeautifulSoup(response.text, 'html.parser')

    
        discount_container = soup.find('div', class_='ProductCard_gcdDiscountContainer__CCi51')

    
        if discount_container:
            price = discount_container.find('span').text.strip()
            return jsonify({'price': price})
        else:
            return jsonify({'error': 'Discount container not found.'}), 404


