# AI Spam & Scam Detector 🕵️‍♂️

An end-to-end Machine Learning pipeline that detects spam, scams, and phishing attempts in real-time. This project uses Natural Language Processing (NLP) and a Naive Bayes classifier to analyze text and calculate a "Spam Probability" score.

The AI is deployed across three different environments: a WhatsApp Bot, a live Gmail background worker, and an interactive Web App.

## Features

* **The Brain:** Custom-trained Naive Bayes ML model using Scikit-Learn (`TF-IDF` vectorization). tuned to a strict 79% confidence threshold to prevent false positives.
* **WhatsApp Bot (`bot.py`):** A live FastAPI server connected to the Twilio Sandbox. Forwards incoming WhatsApp messages to the AI and replies instantly with a safety score.
* **Gmail Guardian (`gmail_spam_bot.py`):** A continuous polling script utilizing the Google Cloud API. It actively monitors an inbox for unread mail, scores them, and automatically banishes spam to the Spam folder.
* **Web UI (`app.py`):** A clean, interactive frontend built with Streamlit for users to manually paste and test suspicious messages.

## Tech Stack
* **Language:** Python
* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **Web Frameworks:** FastAPI, Streamlit, Uvicorn
* **APIs & Integrations:** Twilio (WhatsApp), Google API Client (Gmail)

## How to Run Locally

If you want to run this project on your own machine, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/rushabkarania/Spam-Filter.git](https://github.com/rushabkarania/Spam-Filter.git)
cd Spam-Filter
```

### 2. Set up a virtual environment

**Bash**

```
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
```

### 3. Install dependencies

**Bash**

```
pip install -r requirements.txt
```

### 4. Choose your deployment

**To run the Streamlit Web App:**

**Bash**

```
streamlit run app.py
```

**To run the Gmail Bot:**

*(Note: You must generate your own `credentials.json` from the Google Cloud Console and place it in the root directory first).*

**Bash**

```
python gmail_spam_bot.py
```

**To run the WhatsApp Server:**

*(Note: Requires an active ngrok tunnel and Twilio Developer account).*

**Bash**

```
uvicorn bot:app --reload
```


