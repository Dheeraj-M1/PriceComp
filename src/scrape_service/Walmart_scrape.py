

import requests
from bs4 import BeautifulSoup as soup
import pandas as pd


Input_var = input("choose an item to buy:")
#Input_var=Input_var.capitalize()
input_var=Input_var.replace(" ","+")
print("input_var",input_var)
# The webpage URL

url = "https://www.walmart.com/search?q=z"
URL=url.replace("z",input_var)
print(URL)

#create a url list to scrape data from all pages
url_list = []
for i in range(1,10):
    url_list.append(URL)



#Create empty list to store the data
product_name = []
product_price = []
product_rating = []
product_review = []
for url in url_list:
    result = requests.get(url)
    #print('result',result)
    obj = soup(result.content,'lxml')
    #print('obj',obj)

    extract_name = obj.findAll('div',{'class':'search-result-product-title gridview'})
    extract_rating = obj.findAll('span',{'class':'seo-avg-rating'})
    extract_reviews = obj.findAll('span',{'class':'stars-reviews-count'})
    extract_price = obj.findAll('span',{'class':'price display-inline-block arrange-fit price price-main'})
    
    for names,rating,reviews,price in zip(extract_name,extract_rating,extract_reviews,extract_price):
        extract_name.append(names.a.span.text.strip())
        extract_rating.append(rating.text)
        extract_reviews.append(reviews.text.replace('ratings',''))
        extract_price.append(price.findAll('span',{'class':'visuallyhidden'})[0].text)



#creating a dataframe 

df = pd.DataFrame({'Product_Name':extract_name, 'Price':extract_price, 'Rating':extract_rating,'No_Of_Reviews':extract_reviews}, columns=['Product_Name', 'Price', 'Rating', 'No_Of_Reviews'])
