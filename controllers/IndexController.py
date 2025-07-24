from flask import Blueprint, render_template, request, redirect, url_for
from utils.reddit_fetcher import get_reddit_comments
from utils.sentiment_analyzer import analyse_sentiment
from utils.visualizer import visualize_sentiment_csv

index_blueprint = Blueprint("index", __name__)

@index_blueprint.route("/", methods=["GET"])
def doGet():
    return render_template("index.html")



@index_blueprint.route("/", methods=["POST"])
def doPOST():
    reddit_url = request.form.get("url")

    df = get_reddit_comments(reddit_url)

    if df.empty:
        return render_template("index.html", error="No comments found")
        
    df.to_csv("thread_sentiment_csv", index = False)
    df_sentiment = analyse_sentiment(df)
    df_sentiment.to_csv("Results-sentiment.csv")

    return redirect(url_for('results.doGet'))