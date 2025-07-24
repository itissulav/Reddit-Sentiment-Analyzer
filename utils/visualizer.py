# utils/visualizer.py

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import base64
from io import BytesIO

def visualize_sentiment_csv(csv_path):
    df = pd.read_csv(csv_path)

    # Ensure timestamps are datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # === 1. Sentiment Distribution Pie Chart ===
    sentiment_counts = df['sentiment'].value_counts()
    pie_fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index,
                                     values=sentiment_counts.values,
                                     hole=0.3)])
    pie_fig.update_layout(title_text="Sentiment Distribution")

    # === 2. Average Sentiment Confidence Bar Chart ===
    avg_scores = df[["score_negative", "score_neutral", "score_positive"]].mean()
    bar_fig = px.bar(
        x=avg_scores.index, y=avg_scores.values,
        labels={'x': 'Sentiment Type', 'y': 'Confidence'},
        title="Average Sentiment Confidence",
        color=avg_scores.values, color_continuous_scale='Viridis'
    )

    # === 3. Sentiment Score Distribution Violin Plot ===
    df_melted = df.melt(
        id_vars=["sentiment"],
        value_vars=["score_negative", "score_neutral", "score_positive"],
        var_name="Score Type", value_name="Value"
    )
    violin_fig = px.violin(
        df_melted, x="Score Type", y="Value", color="sentiment",
        box=True, points="all",
        title="Sentiment Score Distribution"
    )

    # === 4. Word Clouds for Each Sentiment ===
    stop_words = set(stopwords.words("english")).union(STOPWORDS)
    wordclouds = {}
    for label in ["Positive", "Neutral", "Negative"]:
        subset = df[df["sentiment"] == label]
        text = " ".join(subset["text"].dropna().astype(str).tolist()).lower()
        wc = WordCloud(
            width=800, height=400, background_color="white",
            stopwords=stop_words, collocations=False
        ).generate(text)
        buffer = BytesIO()
        wc.to_image().save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        wordclouds[label] = f"data:image/png;base64,{img_str}"

    # === 5. Sentiment Counts Over Time (Line Chart) ===
    df['date'] = df['timestamp'].dt.date
    sentiment_daily = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
    sentiment_over_time_fig = px.line(
        sentiment_daily, x='date', y='count', color='sentiment',
        title='Sentiment Counts Over Time (Daily)', markers=True
    )

    # === 6. Average Sentiment Scores Over Time ===
    avg_scores_daily = df.groupby('date')[
        ["score_negative", "score_neutral", "score_positive"]
    ].mean().reset_index()
    avg_scores_daily_fig = go.Figure()
    avg_scores_daily_fig.add_trace(go.Scatter(
        x=avg_scores_daily['date'], y=avg_scores_daily['score_negative'],
        mode='lines+markers', name='Negative'
    ))
    avg_scores_daily_fig.add_trace(go.Scatter(
        x=avg_scores_daily['date'], y=avg_scores_daily['score_neutral'],
        mode='lines+markers', name='Neutral'
    ))
    avg_scores_daily_fig.add_trace(go.Scatter(
        x=avg_scores_daily['date'], y=avg_scores_daily['score_positive'],
        mode='lines+markers', name='Positive'
    ))
    avg_scores_daily_fig.update_layout(
        title='Average Sentiment Scores Over Time',
        xaxis_title='Date', yaxis_title='Score'
    )

    # === 7. Comment Volume Over Time (Hourly) ===
    df['hour'] = df['timestamp'].dt.floor('H')
    comments_per_hour = df.groupby('hour').size().reset_index(name='count')
    comments_over_time_fig = px.bar(
        comments_per_hour, x='hour', y='count',
        title='Number of Comments Per Hour',
        labels={'hour': 'Hour', 'count': 'Number of Comments'}
    )

    # === 8. Heatmap: Negative Sentiment by Weekday & Hour ===
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['weekday'] = df['timestamp'].dt.day_name()
    heatmap_data = df[df['sentiment'] == 'Negative'].groupby(
        ['weekday', 'hour_of_day']
    ).size().reset_index(name='count')
    pivot_data = heatmap_data.pivot(index='hour_of_day', columns='weekday', values='count').fillna(0)
    # Order weekdays
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(columns=days_order)
    heatmap_neg_fig = px.imshow(
        pivot_data,
        labels=dict(x="Weekday", y="Hour of Day", color="Negative Comments"),
        title="Negative Sentiment Heatmap"
    )

    return {
        "pie_fig": pie_fig,
        "bar_fig": bar_fig,
        "violin_fig": violin_fig,
        "wordclouds": wordclouds,
        "sentiment_over_time_fig": sentiment_over_time_fig,
        "avg_scores_daily_fig": avg_scores_daily_fig,
        "comments_over_time_fig": comments_over_time_fig,
        "heatmap_neg_fig": heatmap_neg_fig
    }
