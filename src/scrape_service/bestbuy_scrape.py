from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import pandas as pd
import numpy as np


def get_title(item):
    try:
        return item.find("h4",class_='sku-title').text.strip()
    except AttributeError:
        return np.nan

def get_review(item):
    review_div = item.find("div", class_='ratings-reviews')
    try:
        return float(review_div.find("p", class_="visually-hidden").text.strip().split('out')[0].replace('Rating','').strip())
    except AttributeError:
        return np.nan

def get_sku(item):
    sku_div = item.find("div", class_='sku-attribute-title')
    try:
        return sku_div.find("span", class_='sku-value').text.strip()
    except AttributeError:
        return np.nan

def get_price(item):
    price_div = item.find("div", class_='priceView-hero-price priceView-customer-price')
    try:
        return float(price_div.find("span").text.strip().replace('$','').replace(',',''))
    except (ValueError, AttributeError):
        return np.nan
def get_availability(item):
    try:
        return item.find("div", class_="fulfillment-add-to-cart-button").text.strip()
    except AttributeError:
        return np.nan
    
def get_user_agent():
    f = open('config/headers.json')
    headers = json.load(f)
    user_agent = headers['User-Agent']
    if 'Mozilla/' not in user_agent:
        raise ValueError("Did not add User Agent to config/headers.json")
    else:
        return user_agent

def main(searchText):

    input_var = searchText.replace(" ", "+")
    # The webpage URL
    url = "https://www.bestbuy.com/site/searchpage.jsp?st="
    URL = url + input_var
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    user_agent = get_user_agent()
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(1)
    # driver.get_screenshot_as_file("screenshot.png")
    soup = BeautifulSoup(driver.page_source, "lxml")

    items = soup.find_all("li",class_='sku-item')
    results = []
    for i, item in enumerate(items):
        if i < 2:
            results.append([get_title(item), 'Best Buy',  get_price(item), get_review(item)])
    cols = ['Product Name', 'Marketplace', 'Price ($)', 'Rating (of 5)']
    df = pd.DataFrame(columns=cols, data=results)
    df.dropna(how='any', inplace=True)
    return df
    
    
