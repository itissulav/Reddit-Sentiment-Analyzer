# Reddit Sentiment Analyzer

This is a web-based sentiment analysis tool for Reddit discussions. You can paste the link to a specific Reddit thread, and the app fetches all comments, analyzes them using a transformer-based model (RoBERTa), and visualizes the results with charts and word clouds.

---

## 🔍 Features

- Fetches Reddit thread comments using PRAW
- Filters, cleans, and deduplicates comments
- Performs sentiment analysis using `cardiffnlp/twitter-roberta-base-sentiment`
- Displays results:
  - Pie chart (Sentiment distribution)
  - Bar chart (Average sentiment confidence)
  - Violin plot (Sentiment spread)
  - Word clouds (Positive / Neutral / Negative)
- Easy-to-use web UI using Flask

---

## 🧠 Model Used

- [CardiffNLP RoBERTa Twitter Sentiment Model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)

---

## ⚙️ Requirements

- Python 3.8+
- pip
- Internet connection (to fetch models & Reddit data)

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/reddit-sentiment-analyzer.git
cd reddit-sentiment-analyzer
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
