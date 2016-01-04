#!/usr/bin/env python
#coding=utf-8

import json
import datetime

from flask import Module, Response, request, flash, jsonify, g, current_app,\
    abort, redirect, url_for, session, render_template

from flask.ext.login import login_user,logout_user

from apollo.models import Book,Account
from apollo.extensions import db,login_manager

from books import books

accounts = Module(__name__)

@accounts.route("/register/",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    login_name = request.form['login_name']
    name = request.form['name']
    passwd = request.form['passwd']

    checkAccount = Account.query.filter_by(login_name=login_name).first()

    if checkAccount:
        flash("the username has already exists,please change another one.",'danger')
    else:
        account = Account(login_name,name,passwd)
        account.create_time = datetime.datetime.now().strftime('%Y-%d-%y %H:%M:%S')

        db.session.add(account)
        db.session.commit()

        flash("register success,please login first.","info")

    return redirect(url_for("accounts.login"))


@login_manager.user_loader
def load_user(userid):
    account = Account.query.filter_by(id=userid).first()

    return account

@accounts.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        login_name = request.form['login_name']
        passwd = request.form['passwd']

        if login_name and passwd:
            account = Account.query.filter_by(login_name=login_name).filter_by(passwd=passwd).first()
            
            if account:
                user = Account(account.id,account.name,account.create_time)

                if login_user(account):     
                    return redirect(request.args.get("next") or url_for("books.index"))
            else:
                flash ("Sorry, please check your username or password!","danger")

        else:
            flash ("Sorry, please check your username or password!","danger")
    return render_template("login.html")

@accounts.route("/logout/")
def logout():
    logout_user()
    flash(u"已退出登录.",'info')
    return redirect(url_for("books.index"))

