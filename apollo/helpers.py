#!/usr/bin/env python
#coding=utf-8

import requests
import json
from models import Book

##豆瓣接口api
class DoubanClient():

    def parse_book_info(self,isbn):
        r = requests.get('http://api.douban.com/v2/book/isbn/%s' % isbn)

        jsonObj = json.loads(r.text)

        book = Book()

        if jsonObj['title']:
            book.title = jsonObj['title']
            
            authors = jsonObj['author']
            book.author = ",".join(authors)

            book.price = jsonObj['price']
            book.summary = jsonObj['summary']
            book.catalog = jsonObj['catalog']
            book.publisher = jsonObj['publisher']
            book.isbn13 = jsonObj['isbn13']
            book.douban_id = jsonObj['id']
            book.image = jsonObj['image']
            book.douban_url = jsonObj['alt']
            book.pages = jsonObj['pages']
            book.pubdate = jsonObj['pubdate']
            book.rating = jsonObj['rating']['average']

            book.borrow_id = 0
            book.borrow_name = ''
            book.borrow_counts = 0

        return book

if __name__ == "__main__":
    client = DoubanClient()
    client.parse_book_info("123")
