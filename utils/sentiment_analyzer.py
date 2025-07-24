import pandas as pd
import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.eval()

labels = ['Negative', 'Neutral', 'Positive']

# Set CPU device and max CPU thread usage
device = torch.device("cpu")
torch.set_num_threads(10)
model.to(device)

def analyse_sentiment(df, batch_size=32):
    comment_list = df["text"].tolist()
    results = []

    for i in tqdm(range(0, len(comment_list), batch_size), desc="⚙️ Batched Sentiment Analysis"):
        batch = comment_list[i:i + batch_size]

        # Tokenize batch of comments
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)

        # Process results
        for j, prob in enumerate(probs):
            score, idx = torch.max(prob, dim=0)
            sentiment = labels[idx.item()]
            results.append({
                "sentiment": sentiment,
                "score_negative": prob[0].item(),
                "score_neutral": prob[1].item(),
                "score_positive": prob[2].item(),
            })

    sentiment_df = pd.DataFrame(results)
    combined_df = pd.concat([df.reset_index(drop=True), sentiment_df], axis=1)
    return combined_df
