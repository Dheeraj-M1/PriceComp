
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json

a=[] #Initiallize the list to store search data


# Function to extract Product Title
def extract_title(soup):

    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        title_value = title.string
        title_details = title_value.strip()
    except AttributeError:
        title_details = np.nan
    return title_details

# Function to extract Product Price
def extract_price(soup):
    try:
        price_ID = soup.find('span', 'a-price')
        price = price_ID.find('span', 'a-offscreen').text
    except AttributeError:
        price = np.nan
    return price

# Function to extract Product Rating
def extract_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = np.nan
    return rating

# Function to extract Number of User Reviews
def extract_review(soup):
    try:
        review = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
            review = np.nan

    return review

# Function to extract Availability Status
def extract_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
          available = np.nan
    return available

def get_user_agent():
    f = open('config/headers.json')
    headers = json.load(f)
    user_agent = headers
    if 'Mozilla/' not in user_agent['User-Agent']:
        raise ValueError("Did not add User Agent to config/headers.json")
    else:
        return user_agent

def main(searchText):
   
    HEADERS = get_user_agent()
    #Input_var=Input_var.capitalize()
    input_var=searchText.replace(" ","+")
    print("input_var",input_var)
    # The webpage URL
    url = "https://www.amazon.com/s?k=l"
    URL=url.replace("l",input_var)
    print('URL',URL)

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))
        
    header = ['Product Title','Product Price','Product Rating','Number of Product Reviews','Availability']
    
    # Loop for extracting product details from each link 
    for i, link in enumerate(links_list): 
        if i < 2:     
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "lxml")
            data = [extract_title(new_soup), extract_price(new_soup), extract_rating(new_soup),extract_review(new_soup),extract_availability(new_soup)]
            df = pd.DataFrame (data).transpose()
            df.columns = ['Product Title','Product Price','Product Rating','Number of Product Reviews','Availability']
            
            a.append(data)
    df=pd.DataFrame(a,columns=header)
    df = df[df['Product Rating'].str.contains('stars')]
    df['Product Price']=df['Product Price'].str.replace('$',' ',regex=True).str.replace(',','')
    df['Product Rating']=df['Product Rating'].str.replace('out of','/',regex=True).str.split('/').str[0].astype(float)
    df['Number of Product Reviews']=df['Number of Product Reviews'].str.replace('ratings',' ',regex=True)
    df['Availability']=df['Availability'].str.replace('(more on the way)',' ',regex=True)
    df['Availability']=df['Availability'].str.replace(' - order soon',' ',regex=True)
    df['Availability']=df['Availability'].str.replace('()',' ',regex=True)
    df.rename(columns={'Product Title':'Product Name', 'Product Price':'Price ($)', 'Product Rating':'Rating (of 5)'}, inplace=True)
    df['Marketplace'] = 'Amazon'
    df['Price ($)'] = pd.to_numeric(df['Price ($)'])
    df = df[['Product Name', 'Marketplace', 'Price ($)', 'Rating (of 5)']]
    df.dropna(how='any',inplace=True)
    return df