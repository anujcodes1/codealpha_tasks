"""FAQ chatbot engine.

Pipeline: lowercase -> tokenize (NLTK) -> remove stop-words -> stem (Porter)
-> TF-IDF vectors (scikit-learn) -> cosine similarity against every FAQ question.
"""
import json
import os
import random
import re

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAQ_FILE = os.path.join(BASE_DIR, "faqs.json")

# Small built-in list, used only if the NLTK stop-word corpus cannot be downloaded.
_FALLBACK_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "am", "do", "does", "did",
    "i", "you", "he", "she", "it", "we", "they", "me", "my", "your", "our", "to", "of", "in",
    "on", "at", "for", "with", "and", "or", "but", "if", "then", "so", "can", "could", "would",
    "should", "will", "shall", "this", "that", "these", "those", "have", "has", "had", "what",
    "when", "where", "which", "who", "whom", "how", "why", "there", "here", "about", "as", "by",
}

FILLER_WORDS = {"take", "get", "want", "need", "please", "tell", "know", "like", "wish", "help", "let"}

SMALL_TALK = {
    "greeting": (
        {"hi", "hello", "hey", "hii", "namaste", "good morning", "good evening", "good afternoon"},
        ["Hello! 👋 I'm the ShopEasy assistant. Ask me about orders, delivery, returns or payments.",
         "Hi there! How can I help you today?"],
    ),
    "thanks": (
        {"thanks", "thank you", "thankyou", "thx", "ty"},
        ["You're welcome! Is there anything else I can help with?"],
    ),
    "bye": (
        {"bye", "goodbye", "see you", "exit", "quit"},
        ["Goodbye! Have a great day. 👋"],
    ),
}


def _load_stopwords():
    try:
        from nltk.corpus import stopwords
        try:
            return set(stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("english"))
    except Exception:
        return _FALLBACK_STOPWORDS


class FAQChatbot:
    def __init__(self, faq_path=FAQ_FILE, threshold=0.15):
        with open(faq_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)
        self.threshold = threshold
        self.tokenizer = RegexpTokenizer(r"[a-z0-9]+")
        self.stemmer = PorterStemmer()
        # keep negations (they change meaning); drop filler verbs common in chat
        self.stopwords = (_load_stopwords() - {"not", "no"}) | FILLER_WORDS
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        # Index the question (counted twice for extra weight) plus optional synonym
        # keywords, so rephrased questions still match.
        self.faq_matrix = self.vectorizer.fit_transform(
            [self.preprocess(self._document(item)) for item in self.faqs]
        )

    @staticmethod
    def _document(item):
        q = item["question"]
        return f"{q} {q} {item.get('keywords', '')}"

    def preprocess(self, text):
        """Clean, tokenize, drop stop-words and stem. Returns a space-joined string."""
        tokens = self.tokenizer.tokenize(text.lower())
        tokens = [self.stemmer.stem(t) for t in tokens if t not in self.stopwords]
        return " ".join(tokens)

    def _small_talk(self, message):
        cleaned = re.sub(r"[^a-z ]", "", message.lower()).strip()
        for phrases, replies in SMALL_TALK.values():
            if cleaned in phrases:
                return random.choice(replies)
        return None

    def get_response(self, message):
        """Return (answer, confidence, matched_question)."""
        message = (message or "").strip()
        if not message:
            return "Please type a question and I'll try to help.", 0.0, None

        reply = self._small_talk(message)
        if reply:
            return reply, 1.0, None

        query = self.preprocess(message)
        if not query:
            return "Sorry, I didn't catch that. Could you rephrase your question?", 0.0, None

        scores = cosine_similarity(self.vectorizer.transform([query]), self.faq_matrix)[0]
        best = int(scores.argmax())
        if scores[best] < self.threshold:
            ideas = [self.faqs[i]["question"] for i in scores.argsort()[::-1][:3]]
            hint = "\n".join(f"- {q}" for q in ideas)
            return (
                "Sorry, I couldn't find an exact answer to that. You may be looking for:\n"
                f"{hint}\nOr contact support@shopeasy.example.",
                float(scores[best]),
                None,
            )
        return self.faqs[best]["answer"], float(scores[best]), self.faqs[best]["question"]


def run_cli():
    bot = FAQChatbot()
    print("ShopEasy FAQ Bot - type 'exit' to quit.\n")
    while True:
        try:
            message = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break
        answer, score, matched = bot.get_response(message)
        print(f"Bot: {answer}")
        if matched:
            print(f"     (matched: \"{matched}\" | similarity {score:.2f})")
        if message.strip().lower() in SMALL_TALK["bye"][0]:
            break


if __name__ == "__main__":
    run_cli()
