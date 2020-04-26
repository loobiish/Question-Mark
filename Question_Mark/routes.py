import os
from Question_Mark import app
from flask import render_template, redirect, url_for, flash


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/explore")
def explore():
    return render_template('explore.html', title='Explore')


@app.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ')
























