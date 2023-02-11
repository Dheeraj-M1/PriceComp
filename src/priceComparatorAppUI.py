import time
from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox
from PIL import ImageTk, Image

import backEnd as be

window = Tk()
window.title('PriceComp')
window.geometry("1150x1000")
window.resizable(0, 0)  # Disable minimize/maximize window option, so we can stay on the predefined window size

searchText = StringVar()

chBx0 = StringVar()
chBx1 = StringVar()
chBx2 = StringVar()
chBx3 = StringVar()
rdBttn = IntVar()

def searchProductBox():

    # App Name
    lbl = Label(window, text="Marketplace Price Comparator App\n By S.E.N.D. Team", fg='red', font=("Helvetica", 16))
    lbl.place(relx=0.5, rely=0.1, anchor=CENTER)

    def on_click(event):
        event.widget.delete(0, tk.END)

    # Search Box
    txtfld = Entry(window, width=120, textvariable=searchText, bd=5, justify='center')
    txtfld.bind("<Button-1>", on_click)
    txtfld.insert(0, "Enter a keyword or product SKU #")
    txtfld.pack()
    txtfld.place(relx=0.15, rely=0.20)

def marketPlaceSelectCheckBox():

    c1 = Checkbutton(window, text="", variable=chBx0, onvalue="amazon", offvalue="", height=5, width=20)
    c1.pack(anchor=W)

    c2 = Checkbutton(window, text="", variable=chBx1, onvalue="walmart", offvalue="", height=5, width=20)
    c2.pack(anchor=W)

    c3 = Checkbutton(window, text="", variable=chBx2, onvalue="bestbuy", offvalue="", height=5, width=20)
    c3.pack(anchor=W)

    c4 = Checkbutton(window, text="", variable=chBx3, onvalue="target", offvalue="", height=5, width=20)
    c4.pack(anchor=W)

    c1.place(relx=0.10, rely=0.23)
    c2.place(relx=0.30, rely=0.23)
    c3.place(relx=0.50, rely=0.23)
    c4.place(relx=0.70, rely=0.23)

def insertMarketplaceLogos():
    renderAmazon = ImageTk.PhotoImage(Image.open('assets/amazon.png'))
    renderWalmart = ImageTk.PhotoImage(Image.open('assets/walmart.png'))
    renderBestbuy = ImageTk.PhotoImage(Image.open('assets/bestbuy.png'))
    renderTarget = ImageTk.PhotoImage(Image.open('assets/target.png'))
    imgAmazon = Label(image=renderAmazon)
    imgAmazon.image = renderAmazon
    imgAmazon.place(relx=0.12, rely=0.32, anchor=W)
    imgWalmart = Label(image=renderWalmart)
    imgWalmart.image = renderWalmart
    imgWalmart.place(relx=0.32, rely=0.32, anchor=W)
    imgBestbuy = Label(image=renderBestbuy)
    imgBestbuy.image = renderBestbuy
    imgBestbuy.place(relx=0.52, rely=0.32, anchor=W)
    imgTarget = Label(image=renderTarget)
    imgTarget.image = renderTarget
    imgTarget.place(relx=0.72, rely=0.32, anchor=W)

def searchButton():

    btn = Button(window, text="Search", command=lambda: [be.runScrape(searchText.get(), [chBx0.get(), chBx1.get(), chBx2.get(), chBx3.get()]),
                                                         searchResultTable(sort=False, attributeIdx=-1)])
    btn.pack()
    btn.place(relx=0.80, rely=0.2)

    # Populate the search results in the table

def searchResultTable(sort, attributeIdx):

    print('attributeIdx =', attributeIdx)

    # Search Result Table Headers
    productDetailsTable = [['Product Name', 'Marketplace', 'Price ($)', 'Rating (/5.0)']]
    # print(productDetailsTable)
    searchResults = be.unSortedSearchResults()
    if(sort == True):
        if(attributeIdx == 0 or attributeIdx == 1):
            if(attributeIdx == 1):
                searchResults.sort(key=lambda x: x[2], reverse=True)
            else:
                searchResults.sort(key=lambda x: x[2], reverse=False)
        elif(attributeIdx == 2 or attributeIdx == 3):
            if(attributeIdx == 3):
                searchResults.sort(key=lambda x: x[3], reverse=True)
            else:
                searchResults.sort(key=lambda x: x[3], reverse=False)

    print('Sorted result table =', searchResults)
    for item in searchResults:
        productDetailsTable.append(item)
    # print('Product details = ', productDetailsTable)

    # find total number of rows and columns in list
    total_rows = len(productDetailsTable)
    total_columns = len(productDetailsTable[0])

    # Adding Headers first in the table in the UI
    for i in range(1):
        temp = float(i)
        for j in range(total_columns):
            temp1 = float(j)
            if (j == 0):
                tblEnty = Entry(window, width=60, fg='red', font=('Arial', 10, 'bold'))
            else:
                tblEnty = Entry(window, width=15, fg='red', font=('Arial', 10, 'bold'))

            if(j > 0):
                tblEnty.place(relx=(0.30 + temp1 / 5.0), rely=(0.60 + temp / 20.0), anchor=CENTER)
            else:
                tblEnty.place(relx=(0.20 + temp1 / 5.0), rely=(0.60 + temp / 20.0), anchor=CENTER)
            tblEnty.insert(END, productDetailsTable[i][j].upper())

    # Adding Product Data
    for i in range(total_rows):
        temp = float(i)
        for j in range(total_columns):
            if i != 0:
                temp1 = float(j)
                if (j == 0):
                    tblEnty = Entry(window, width=60, fg='blue', font=('Arial', 10, 'bold'))
                else:
                    tblEnty = Entry(window, width=15, fg='blue', font=('Arial', 10, 'bold'))
                if (j > 0):
                    tblEnty.place(relx=(0.30 + temp1 / 5.0), rely=(0.60 + temp / 20.0), anchor=CENTER)
                else:
                    tblEnty.place(relx=(0.20 + temp1 / 5.0), rely=(0.60 + temp / 20.0), anchor=CENTER)
                tblEnty.insert(END, productDetailsTable[i][j])

    # print('temp and temp1 = ', temp, temp1)

def sortOptionSelectCheckBox():

    rb1 = Radiobutton(window, text="Price\nLow to High", variable=rdBttn, value=0, height=5, width=20)
    rb1.pack(anchor=W)

    rb2 = Radiobutton(window, text="Price\nHigh to Low", variable=rdBttn, value=1, height=5, width=20)
    rb2.pack(anchor=W)

    rb3 = Radiobutton(window, text="Rating\nLow to High", variable=rdBttn, value=2, height=5, width=20)
    rb3.pack(anchor=W)

    rb4 = Radiobutton(window, text="Rating\nHigh to Low", variable=rdBttn, value=3, height=5, width=20)
    rb4.pack(anchor=W)

    rb1.place(relx=0.16, rely=0.4)
    rb2.place(relx=0.36, rely=0.4)
    rb3.place(relx=0.56, rely=0.4)
    rb4.place(relx=0.76, rely=0.4)

def sortButton():

    btn = Button(window, text="Sort Result By:", command=lambda: searchResultTable(sort=True, attributeIdx=rdBttn.get()))

    btn.pack()
    btn.place(relx=0.06, rely=0.425)

    # Populate the search results in the table

def uIWindowsConfig():
    window.mainloop()

if __name__ == '__main__':

    marketPlaceSelectCheckBox()
    searchProductBox()
    searchButton()
    sortOptionSelectCheckBox()
    sortButton()
    insertMarketplaceLogos()
    uIWindowsConfig()
