#!/usr/bin/env python
#coding=utf-8

import requests
import json
import datetime

from flask import Module, Response, request, flash, jsonify, g, current_app,\
    abort, redirect, url_for, session, render_template

from flask.ext.login import login_required,current_user
from sqlalchemy import or_

from apollo.models import Book,BorrowLog,Tag,BookTag
from apollo.extensions import db
from apollo.helpers import DoubanClient

books = Module(__name__)

# 首页
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
            page_obj = Book.query.order_by(Book.id.desc()).paginate(page, Book.PER_PAGE, False)
        else:
            page_obj = Book.query.filter(or_(Book.title.ilike('%'+keywords+"%"),Book.author.ilike('%'+keywords+"%"),Book.owner_name.ilike('%'+keywords+"%"))).order_by(Book.id.desc()).paginate(page, Book.PER_PAGE, False)
    else:
        page_obj = Book.query.paginate(page, Book.PER_PAGE, False)

    return render_template("index.html",q = keywords, page_obj = page_obj)

# 个人主页
@books.route("/my/", methods=("GET","POST"))
@login_required
def my():
    current_borrow_book = Book.query.filter_by(borrow_id=current_user.id).first()
    share_book_list = Book.query.filter_by(owner_id=current_user.id).order_by(Book.id.desc()).limit(10)

    #借阅历史
    borrow_log_list = BorrowLog.query.filter_by(account_id = current_user.id).order_by(BorrowLog.id.desc()).limit(10)

    return render_template("my_books.html", 
            current_borrow_book = current_borrow_book,
            share_book_list = share_book_list,
            borrow_log_list = borrow_log_list
        )

# 查看单个图书详情
@books.route("/<int:book_id>/", methods=("GET","POST"))
def view(book_id):

    book = Book.query.filter_by(id = book_id).first()

    #借阅历史
    borrow_log_list = BorrowLog.query.filter_by(book_id = book.id).order_by(BorrowLog.id.desc()).limit(10)

    return render_template("book_detail.html", 
        book = book,
        borrow_log_list = borrow_log_list)

# 获取豆瓣图书信息
@books.route("/douban_book_info/", methods=("GET","POST"))
def douban_book_info():
    isbn = request.args.get('isbn', '')
    print "douban_book_info , isbn=",isbn

    r = requests.get('http://api.douban.com/v2/book/isbn/%s' % isbn)

    return r.text

# 我要分享
@books.route("/share/", methods=("GET","POST"))
@login_required
def share():
    if request.method == "GET":
        return render_template("share.html")
    isbn = request.form['isbn']
    client = DoubanClient()
    book = client.parse_book_info(isbn)

    print current_user.name

    if book:
        book.owner_id = current_user.id
        book.owner_name = current_user.name
        
        db.session.add(book)
        db.session.commit()

        for tag in book.tags:
            t = Tag.query.filter_by(name = tag['name'].encode('utf-8')).first()
            if not t: # 如果以前不存在
                t = Tag()
                t.name = tag['name']
                t.counts = int(tag['count'])
                t.create_time = datetime.datetime.now().strftime('%Y-%m-%y %H:%M:%S')
                db.session.add(t)
                db.session.commit()
            else:
                t.counts = t.counts + int(tag['count'])

            bookTag = BookTag()
            bookTag.book_id = book.id
            bookTag.tag_id = t.id
            bookTag.count = tag['count']
            db.session.add(bookTag)
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

# 还书
@books.route("/reback/<int:book_id>/", methods=("GET","POST"))
def reback(book_id):
    print "reback book , book_id=",book_id

    book = Book.query.filter_by(id = book_id).first()

    # 修改图书属性
    book.borrow_id = None
    book.borrow_name = ''

    #记录还书时间
    borrow_log = BorrowLog.query.filter_by(id = book.borrow_log_id).first()
    borrow_log.real_reback_time = datetime.datetime.now().strftime('%Y-%m-%y %H:%M:%S')

    db.session.commit()
    
    
    flash(u"还书成功，好借好还，再借不难。","info")
    return redirect(url_for("books.my"))

# 借书
@books.route("/borrow/<int:book_id>/", methods=("GET","POST"))
def borrow(book_id):
    print "borrow book , book_id=",book_id

    # 检查当前用户是否存在未还的图书，同一时间只允许借一本书
    checkBook = Book.query.filter_by(borrow_id = current_user.id).first()
    if checkBook:
        flash(u"借书失败，你当前还有未还的图书，不要太贪心。","danger")
        return redirect(url_for("books.view",book_id=book_id))

    # 修改图书的相关属性
    book = Book.query.filter_by(id = book_id).first()

    # 检查当前图书的状态，如果被别人借阅中，则不能借入


    # 记入借阅历史
    borrow_log = BorrowLog(current_user.id,current_user.name,book_id,book.title)
    borrow_log.create_time = datetime.datetime.now().strftime('%Y-%m-%y %H:%M:%S')
    borrow_log.reback_time = (datetime.datetime.now()+datetime.timedelta(days=14)).strftime('%Y-%m-%y')

    db.session.add(borrow_log)

    #这一行不能删，首先保存之后，可以获取borrow_log的ID
    db.session.commit()
    
    book.borrow_id = current_user.id
    book.borrow_name = current_user.name
    book.borrow_counts += 1
    book.borrow_log_id = borrow_log.id
    book.status = 1 #借书成功，设置状态为借阅中

    db.session.commit()

    flash(u"借书成功，请一定要按时归还吆。","danger")
    return redirect(url_for("books.my"))
