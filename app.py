import os

import psycopg2
from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)

sentiment_pipeline = pipeline("sentiment-analysis")


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "sentiment_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
    return conn


@app.route("/predict", methods=["POST"])
def predict_sentiment():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = sentiment_pipeline(text)[0]
    sentiment = result["label"]
    score = result["score"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (text, sentiment, score) VALUES (%s, %s, %s)",
        (text, sentiment, score),
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"sentiment": sentiment, "score": score})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
