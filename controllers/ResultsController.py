from flask import Blueprint, render_template
from utils.visualizer import visualize_sentiment_csv
import plotly.io as pio

results_blueprint = Blueprint("results", __name__)

@results_blueprint.route("/results", methods=["GET"])
def doGet():
    figs = visualize_sentiment_csv("Results-sentiment.csv")

    return render_template("results.html",
        pie_html=pio.to_html(figs["pie_fig"], full_html=False),
        bar_html=pio.to_html(figs["bar_fig"], full_html=False),
        violin_html=pio.to_html(figs["violin_fig"], full_html=False),
        sentiment_over_time_html=pio.to_html(figs["sentiment_over_time_fig"], full_html=False),
        avg_scores_daily_html=pio.to_html(figs["avg_scores_daily_fig"], full_html=False),
        comments_over_time_html=pio.to_html(figs["comments_over_time_fig"], full_html=False),
        heatmap_neg_html=pio.to_html(figs["heatmap_neg_fig"], full_html=False),
        wordclouds=figs["wordclouds"]
    )
