from flask import Flask, request, render_template_string
from textblob import TextBlob
from transformers import pipeline
import re

app = Flask(__name__)

# AI emotion detection using PyTorch
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1,
    framework="pt"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>NLP Grammar & Emotion Analyzer</title>
<style>
body{
    font-family:Arial;
    background:#101827;
    color:white;
    text-align:center;
    padding:40px
}
textarea{
    width:80%;
    height:180px;
    padding:15px;
    border-radius:10px;
    font-size:16px
}
button{
    padding:12px 30px;
    margin:20px;
    background:#38bdf8;
    border:0;
    border-radius:8px;
    font-weight:bold;
    cursor:pointer
}
.card{
    background:#1e293b;
    padding:25px;
    margin:20px auto;
    max-width:800px;
    border-radius:15px
}
.result{
    font-size:24px;
    font-weight:bold
}
</style>
</head>

<body>

<h1>NLP Grammar & Emotion Analyzer</h1>

<p>AI-Powered Grammar Checking and Emotion Detection</p>

<form method="POST">

<textarea
name="text"
placeholder="Enter your text here..."
required>{{ text }}</textarea>

<br>

<button>Analyze Text</button>

</form>

{% if result %}

<div class="card">

<h2>Emotion</h2>
<div class="result">{{ emotion }}</div>
<p>Confidence: {{ confidence }}%</p>

<h2>Sentiment</h2>
<div class="result">{{ sentiment }}</div>

<h2>Grammar Errors</h2>
<div class="result">{{ errors }}</div>

<h2>Corrected Text</h2>
<p>{{ corrected }}</p>

</div>

{% endif %}

</body>
</html>
"""


def detect_emotion(text):
    result = emotion_model(text)

    # Handle different Transformers output formats
    while isinstance(result, list):
        result = result[0]

    emotion = result["label"]
    confidence = result["score"]

    return emotion, round(confidence * 100, 2)

def grammar_check(text):

    errors = 0
    corrected = text

    rules = {
        r"\bi is\b": "I am",
        r"\bhe are\b": "he is",
        r"\bshe are\b": "she is",
        r"\bthey is\b": "they are",
        r"\byou is\b": "you are",
        r"\bwe is\b": "we are",
        r"\bi has\b": "I have",
        r"\bhe have\b": "he has",
        r"\bshe have\b": "she has"
    }

    for pattern, replacement in rules.items():

        if re.search(pattern, corrected, re.IGNORECASE):

            errors += 1

            corrected = re.sub(
                pattern,
                replacement,
                corrected,
                flags=re.IGNORECASE
            )

    return corrected, errors


@app.route("/", methods=["GET", "POST"])
def home():

    result = False
    text = ""
    corrected = ""
    errors = 0
    emotion = ""
    confidence = 0
    sentiment = ""

    if request.method == "POST":

        result = True

        text = request.form["text"]

        corrected, errors = grammar_check(text)

        emotion, confidence = detect_emotion(text)

        polarity = TextBlob(text).sentiment.polarity

        if polarity > 0.1:
            sentiment = "Positive"

        elif polarity < -0.1:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

    return render_template_string(
        HTML,
        result=result,
        text=text,
        corrected=corrected,
        errors=errors,
        emotion=emotion,
        confidence=confidence,
        sentiment=sentiment
    )


if __name__ == "__main__":
    app.run(
        debug=False,
        port=5000
    )