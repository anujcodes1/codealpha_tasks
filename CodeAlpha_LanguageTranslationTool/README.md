# 🌐 Language Translation Tool

**CodeAlpha Artificial Intelligence Internship - Task 1**

A web app where you type text, pick a source and target language, and get the translation instantly.
Built with Python and Streamlit, using the Google Translate service through `deep-translator`.

## Features
- Text input with 100+ supported languages
- **Auto-detect** source language
- Clear translated output with a one-click **copy button**
- **Text-to-speech** playback of the translation (gTTS)
- Input validation and friendly error messages (empty text, text too long, no internet)

## Tech stack
Python · Streamlit · deep-translator (Google Translate) · gTTS

## Project structure
```
├── app.py            # Streamlit user interface
├── translator.py     # Translation + text-to-speech logic
├── requirements.txt
└── README.md
```

## Setup & run
```bash
git clone https://github.com/anujcodes1/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501. An internet connection is required for translation.

## How it works
1. The user enters text and selects source and target languages.
2. `translator.translate_text()` validates the input and sends it to the Google Translate service.
3. The translated text is displayed with a copy button, and can be played back using gTTS.

## Author
Anuj Mishra - [GitHub](https://github.com/anujcodes1)

#CodeAlpha
