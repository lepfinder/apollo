#!/usr/bin/env python
#coding=utf-8

from apollo.extensions import db


class BorrowLog(db.Model):
    __tablename__ = 'borrow_log'

    id = db.Column(db.Integer,primary_key=True)

    account_id = db.Column(db.Integer)
    account_name = db.Column(db.String(64))
    book_id = db.Column(db.Integer)
    book_name = db.Column(db.String(128))
    create_time = db.Column(db.DateTime)
    real_reback_time = db.Column(db.DateTime)

    def __init__(self,account_id,account_name,book_id,book_name):
        self.account_id = account_id
        self.account_name = account_name
        self.book_id = book_id
        self.book_name = book_name


