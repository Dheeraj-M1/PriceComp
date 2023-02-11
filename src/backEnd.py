import pandas as pd
from scrape_service import bestbuy_scrape as bb_scrape
from scrape_service import target_scrape as t_scrape
from scrape_service import amazon_scrape as a_scrape

# Product Data
productData = pd.DataFrame()

# Retrieve search keyword and checkbox data and run scraping accordingly
def runScrape(searchText, selectBoxList):
    global productData 
    dfs = []
    for item in selectBoxList:
        if item == 'bestbuy':
            dfs.append(bb_scrape.main(searchText))
        elif item == 'target':
            dfs.append(t_scrape.main(searchText))
        elif item == 'amazon':
            dfs.append(a_scrape.main(searchText))
        elif item == 'walmart':
            print('walmart scraping is currently unavailable due to bot detection')
    if len(dfs) != 0:
        productData = pd.concat(dfs, ignore_index=True)

def unSortedSearchResults():

    # Convert dataframe to List to use in the UI result table
    lst = productData.values.tolist()

    return lst


   


