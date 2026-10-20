# 💬 FAQ Chatbot

**CodeAlpha Artificial Intelligence Internship - Task 2**

A chatbot that answers customer questions for a sample online store (**ShopEasy**). It preprocesses text with
NLTK, converts questions into TF-IDF vectors, and returns the answer of the most similar FAQ using cosine similarity.

## Features
- 24 FAQs on orders, delivery, returns, payments, accounts and support (`faqs.json` - easy to edit or replace)
- Each FAQ is indexed by its question plus synonym keywords, so rephrased questions still match
- NLP preprocessing: lowercase → tokenize → stop-word removal → stemming (NLTK)
- TF-IDF (unigrams + bigrams) with **cosine similarity** matching (scikit-learn)
- Confidence threshold: if nothing matches well, the bot suggests the 3 closest questions
- Small-talk handling (hello, thanks, bye)
- Two interfaces: **Streamlit chat UI** and a **command-line** chat

## Tech stack
Python · NLTK · scikit-learn · Streamlit

## Project structure
```
├── app.py            # Streamlit chat UI
├── chatbot.py        # NLP pipeline + matching engine (also runs as a CLI)
├── faqs.json         # FAQ knowledge base
├── requirements.txt
└── README.md
```

## Setup & run
```bash
git clone https://github.com/anujcodes1/CodeAlpha_FAQChatbot.git
cd CodeAlpha_FAQChatbot
pip install -r requirements.txt

streamlit run app.py      # chat UI at http://localhost:8501
python chatbot.py         # or: command-line chat
```

## How it works
1. **Preprocess** each FAQ question and the user's message the same way (clean, tokenize, remove stop-words, stem).
2. **Vectorize** with TF-IDF so important words get more weight.
3. **Compare** the user's vector with every FAQ vector using cosine similarity.
4. **Respond** with the best answer if its score is above the threshold (0.15), otherwise suggest related questions.

## Use your own FAQs
Edit `faqs.json`, keeping the format `{"question": "...", "answer": "...", "keywords": "optional synonyms"}`. No code changes needed.

## Author
Anuj Mishra - [GitHub](https://github.com/anujcodes1)

#CodeAlpha
