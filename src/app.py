# -*- coding: utf-8 -*-

# ------------------------------------------ Module Imports & Definitions -------------------------------------------- #

# Standard package(s) import ----------------------------------------------------------------------
import os
import flask
from flask import send_file

# Project packages(s) import ----------------------------------------------------------------------
from src.top10_categories import *
from src.paper_keywords import *


# ------------------------------------------- App and Routes Definition ---------------------------------------------- #
# initialise flask app
app = flask.Flask(__name__)

# add route to get top10 categories
@app.route("/top10_categories", methods=["GET"])
def top10_cat():
    """Instantiate Top10 class and compute top10 categories for last year.

    :return: string giving top10 categories.
    """
    # path to database
    db_path = './../data/arxiv.db'
    # instantiate Top10 src
    top10 = Top10(db_path)
    # query appropriate columns on top10 object
    top10.query_columns('ARXIV', ['categories', 'versions'])
    # extract year from versions dates
    top10.extract_version_year()
    # compute top10 categories
    top10.top10_categories(2020)
    # return top 10 categories
    return top10.display


@app.route("/keywords_txt/<paper_id>", methods=["GET"])
def kw_txt(paper_id):
    """Start a prediction with the trained model on the given year.

    :return: prediction features and labels
    """
    # instantiate Keywords src
    paper_kw = Keywords(str(paper_id), 20)
    # download paper for paper_kw instance
    paper_kw.dl_paper()
    # create and display wordcloud on paper
    paper_kw.wordcloud()
    # find main keywords from paper
    paper_kw.find_keywords()
    # delete downloaded paper
    paper_kw.remove_pdf()
    # display main keywords from paper
    return paper_kw.display


@app.route("/keywords_im/<paper_id>", methods=["GET"])
def kw_im(paper_id):
    """Start a prediction with the trained model on the given year.

    :return: prediction features and labels
    """
    # instantiate Keywords src
    paper_kw = Keywords(str(paper_id), 20)
    # download paper for paper_kw instance
    paper_kw.dl_paper()
    # create and display wordcloud on paper
    paper_kw.wordcloud()
    # find main keywords from paper
    paper_kw.find_keywords()
    # delete downloaded paper
    paper_kw.remove_pdf()
    # display main keywords from paper
    return send_file('wordcloud.png', mimetype='image/png')


app.run(host='localhost', port=80)
