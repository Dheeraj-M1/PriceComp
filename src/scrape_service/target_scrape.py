from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd
import numpy as np
import json

def get_title(item):
    try:
        return item.find("div",class_='h-display-flex').text.strip()
    except AttributeError:
        return np.nan

def get_image (item):
    element = item.find("img")
    try:
        return element['src']
    except AttributeError:
        return np.nan

def get_review(item):
    search_re = re.compile('.*RatingStars__RatingStarsContainer.*')
    item = item.find("div", {"class" : search_re})
    search_re_span = re.compile('.*utils__ScreenReaderOnly-sc.*')
    try:
        return float(item.find("span", class_=search_re_span).text.strip().split('out')[0].strip())
    except AttributeError:
        return np.nan

def get_price(item):
    search_re = re.compile('.*styles__PriceStandardLineHeight-sc.*')
    try:
        return float(item.find("div", class_=search_re).span.text.strip().replace('$','').replace(',',''))
    except AttributeError:
        return np.nan

def get_availability(item):
    search_re = re.compile('.*styles__StyledCartAndTryOnButtons-sc.*')
    try:
        return item.find("div", class_=search_re).text.strip()
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
    url = "https://www.target.com/s?searchTerm="
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
    time.sleep(4)
    # driver.get_screenshot_as_file("screenshot.png")
    soup = BeautifulSoup(driver.page_source, "lxml")
    search_row_re = re.compile('.*styles__StyledRow-sc.*')
    search_col_re = re.compile('.*styles__StyledCol.*')
    row_wrapper = soup.find_all("div", {'class':search_row_re})
    item_wrapper = row_wrapper[5]
    items = item_wrapper.find_all("div", {'class':search_col_re})
    results = []
    for i, item in enumerate(items):
        if i < 2:
            results.append([get_title(item), 'Target',  get_price(item), get_review(item)])
    cols = ['Product Name', 'Marketplace', 'Price ($)', 'Rating (of 5)']
    df = pd.DataFrame(columns=cols, data=results)
    df.dropna(how='any', inplace=True)
    return df
