import requests
from bs4 import BeautifulSoup
import sqlite3

URL = "https://books.toscrape.com/"

# git config --global user.name "def-uxaamod"
# git config --global user.email "lamichhanez.aamod69x@gmail.com"


def scrap_book(url):
    response = requests.get(url)
    print(response.status_code)
    if response.status_code!=200:
        print("Failed to fetch the page,status code:{}".format(response.status_code))
        return 
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text,"html.parser")
    books = soup.find_all("article",class_="product_pod")
    print(books)

    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p",class_="price_color").text
        currency = price_text[0]
        price = price_text[1:]
        insert_book(title,currency,price)


def create_database():
    con = sqlite3.connect("books_details.sqlite3")
    cur = con.cursor()

    cur.execute(
        '''
        create table if not exists books(
            id integer primary key autoincrement,
            Bookname char(100) not null,
            Currency char(100) not null,
            Price integer not null
        )
        '''
    )
    con.commit()
    con.close()

def insert_book(title,currency,price):
    con = sqlite3.connect("books_details.sqlite3")
    cur = con.cursor()
    cur.execute(
        '''
            insert into books(Bookname,Currency,Price)
            values
            (?,?,?)
    '''
    ,(title,currency,price)
    )
    con.commit()
    con.close()
    
create_database()
scrap_book(URL)