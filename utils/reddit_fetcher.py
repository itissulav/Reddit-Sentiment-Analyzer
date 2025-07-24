# utils/reddit_fetcher.py

import os
import praw
from dotenv import load_dotenv
import pandas as pd
from transformers import AutoTokenizer
from datetime import datetime

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

def get_reddit_comments(url):
    clean_url = list(filter(None, url.split('/')))
    post_id = clean_url[-2]
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)

    all_comments = submission.comments.list()
    comment_data = []

    for comment in all_comments:
        cleaned = comment.body.replace('\n', ' ').strip()
        tokenized = tokenizer.encode(cleaned, truncation=False)
        if len(tokenized) > 512:
            continue

        # Convert UTC to readable datetime
        timestamp = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')

        comment_data.append({
            "text": cleaned,
            "score": comment.score,
            "timestamp": timestamp
        })

    return pd.DataFrame(comment_data)
