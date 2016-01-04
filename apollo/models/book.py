#!/usr/bin/env python
#coding=utf-8

from apollo.extensions import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer,primary_key=True)

    PER_PAGE = 12

    title = db.Column(db.String(64))

    isbn13 = db.Column(db.String(64))
    author = db.Column(db.String(64))
    rating = db.Column(db.Float)
    pubdate = db.Column(db.String(16))
    image = db.Column(db.String(128))
    douban_id = db.Column(db.Integer)
    publisher = db.Column(db.String(64))
    douban_url = db.Column(db.String(128))
    summary = db.Column(db.Text)
    price = db.Column(db.String(32))
    pages = db.Column(db.String(32))
    catalog = db.Column(db.Text)
    owner_name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer)
    borrow_name = db.Column(db.String(64))
    borrow_id = db.Column(db.Integer)
    borrow_log_id = db.Column(db.Integer)
    borrow_counts = db.Column(db.Integer)



