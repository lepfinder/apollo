#!/usr/bin/env python
#coding=utf-8

import requests
import json
import datetime

from flask import Module, Response, request, flash, jsonify, g, current_app,\
    abort, redirect, url_for, session, render_template

from flask.ext.login import login_required,current_user
from sqlalchemy import or_

from apollo.models import Book,BorrowLog
from apollo.extensions import db

books = Module(__name__)

@books.route("/", methods=("GET","POST"))
def index():
    page = 1
    keywords = ''

    if request.method == "POST":
        page = request.form['page']
        keywords = request.form['q']

        page = int(page) if page else 1

        print "keywords=",keywords,"page=",page
        if not keywords:
            page_obj = Book.query.paginate(page, Book.PER_PAGE, False)
        else:
            page_obj = Book.query.filter(or_(Book.title.ilike('%'+keywords+"%"),Book.author.ilike('%'+keywords+"%"),Book.owner_name.ilike('%'+keywords+"%"))).paginate(page, Book.PER_PAGE, False)
    else:
        page_obj = Book.query.paginate(page, Book.PER_PAGE, False)

    return render_template("index.html",q = keywords, page_obj = page_obj)



@books.route("/my/", methods=("GET","POST"))
@login_required
def my():
    borrow_book_list = Book.query.filter_by(borrow_id=current_user.id).limit(10)
    share_book_list = Book.query.filter_by(owner_id=current_user.id).limit(10)

    #借阅历史
    borrow_log_list = BorrowLog.query.filter_by(account_id = current_user.id).order_by(BorrowLog.id.desc()).limit(10)

    return render_template("my_books.html", 
            borrow_book_list = borrow_book_list,
            share_book_list = share_book_list,
            borrow_log_list = borrow_log_list
        )

@books.route("/<int:book_id>/", methods=("GET","POST"))
def view(book_id):

    book = Book.query.filter_by(id = book_id).first()

    #借阅历史
    borrow_log_list = BorrowLog.query.filter_by(book_id = book.id).order_by(BorrowLog.id.desc()).limit(10)

    return render_template("book_detail.html", 
        book = book,
        borrow_log_list = borrow_log_list)



@books.route("/douban_book_info/", methods=("GET","POST"))
def douban_book_info():
    isbn = request.args.get('isbn', '')
    print "douban_book_info , isbn=",isbn

    r = requests.get('http://api.douban.com/v2/book/isbn/%s' % isbn)

    return r.text

@books.route("/share/", methods=("GET","POST"))
@login_required
def share():
    if request.method == "GET":
        return render_template("share.html")

    isbn = request.form['isbn']
    r = requests.get('http://api.douban.com/v2/book/isbn/%s' % isbn)

    jsonObj = json.loads(r.text)

    book = Book()

    print current_user.name

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

        book.owner_id = current_user.id
        book.owner_name = current_user.name
        book.borrow_id = 0
        book.borrow_name = ''
        book.borrow_counts = 0

        db.session.add(book)
        db.session.commit()

        res = {
            "code" : 200,
            "message" : "分享成功"
        }
    else:
        res = {
            "code" : 400,
            "message" : "分享失败"
        }

    return jsonify(res)


@books.route("/reback/", methods=("GET","POST"))
def reback():
    book_id = request.form['book_id']
    print "reback book , book_id=",book_id

    book = Book.query.filter_by(id = book_id).first()

    # 修改图书属性
    book.borrow_id = None
    book.borrow_name = ''

    #记录还书时间
    borrow_log = BorrowLog.query.filter_by(id = book.borrow_log_id).first()
    borrow_log.real_reback_time = datetime.datetime.now().strftime('%Y-%d-%y %H:%M:%S')

    db.session.commit()
    res = {
        "code" : 200,
        "message" : "操作成功"
    }

    return jsonify(res)



@books.route("/borrow/", methods=("GET","POST"))
def borrow():
    book_id = request.form['book_id']
    print "borrow book , book_id=",book_id
    # 修改图书的相关属性
    book = Book.query.filter_by(id = book_id).first()


    # 记入借阅历史
    borrow_log = BorrowLog(current_user.id,current_user.name,book_id,book.title)
    borrow_log.create_time = datetime.datetime.now().strftime('%Y-%d-%y %H:%M:%S')

    db.session.add(borrow_log)

    
    book.borrow_id = current_user.id
    book.borrow_name = current_user.name
    book.borrow_counts += 1
    book.borrow_log_id = borrow_log.id

    db.session.commit()


    res = {
        "code" : 200,
        "message" : "操作成功"
    }

    return jsonify(res)
