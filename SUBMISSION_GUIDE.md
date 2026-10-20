# CodeAlpha AI Internship - Submission Guide

Tasks built (3 of 4; the minimum required is 2):
1. `CodeAlpha_LanguageTranslationTool`  (Task 1)
2. `CodeAlpha_FAQChatbot`               (Task 2)
3. `CodeAlpha_ObjectDetectionTracking`  (Task 4)

Each folder is its own GitHub repository (the PDF asks for repo name `CodeAlpha_ProjectName`).

## STEP 1 - Create 3 EMPTY repos on github.com
New repository -> Public -> NO README -> names exactly:
CodeAlpha_LanguageTranslationTool, CodeAlpha_FAQChatbot, CodeAlpha_ObjectDetectionTracking

## STEP 2 - Push each project (PowerShell, from this folder)
```powershell
cd CodeAlpha_LanguageTranslationTool
git init
git add .
git commit -m "CodeAlpha AI internship - Task 1: Language Translation Tool"
git branch -M main
git remote add origin https://github.com/anujcodes1/CodeAlpha_LanguageTranslationTool.git
git push -u origin main
cd ..

cd CodeAlpha_FAQChatbot
git init
git add .
git commit -m "CodeAlpha AI internship - Task 2: FAQ Chatbot"
git branch -M main
git remote add origin https://github.com/anujcodes1/CodeAlpha_FAQChatbot.git
git push -u origin main
cd ..

cd CodeAlpha_ObjectDetectionTracking
git init
git add .
git commit -m "CodeAlpha AI internship - Task 4: Object Detection and Tracking"
git branch -M main
git remote add origin https://github.com/anujcodes1/CodeAlpha_ObjectDetectionTracking.git
git push -u origin main
cd ..
```

## STEP 3 - Record a short demo video of each project
```powershell
pip install -r requirements.txt     # inside each project folder
streamlit run app.py                # Task 1 and Task 2
python detect_track.py              # Task 4 (webcam)  or  --source yourvideo.mp4
```
Screen-record 1-2 minutes each (Windows: Win + G, or OBS). Show the app working and briefly explain the code.

## STEP 4 - LinkedIn posts (tag @CodeAlpha, add repo link, attach video)

**Task 1 post**
Excited to share my Task 1 for the @CodeAlpha Artificial Intelligence Internship: a Language Translation Tool! 🌐
✅ 100+ languages with auto-detect
✅ One-click copy and text-to-speech
✅ Built with Python, Streamlit and Google Translate
GitHub: https://github.com/anujcodes1/CodeAlpha_LanguageTranslationTool
#CodeAlpha #AI #Python #Internship #MachineLearning #NLP

**Task 2 post**
Task 2 of my @CodeAlpha AI Internship: an FAQ Chatbot! 💬
✅ NLTK preprocessing (tokenize, stop-words, stemming)
✅ TF-IDF + cosine similarity to find the best answer
✅ Chat UI built with Streamlit
GitHub: https://github.com/anujcodes1/CodeAlpha_FAQChatbot
#CodeAlpha #AI #NLP #Python #Chatbot #Internship

**Task 4 post**
Task 4 of my @CodeAlpha AI Internship: real-time Object Detection and Tracking! 🎯
✅ YOLOv8 detection + ByteTrack tracking (SORT family)
✅ Unique tracking IDs, labels and movement trails
✅ Works on webcam and video files with OpenCV
GitHub: https://github.com/anujcodes1/CodeAlpha_ObjectDetectionTracking
#CodeAlpha #ComputerVision #YOLO #OpenCV #AI #Internship

## STEP 5 - Submission form (shared in your WhatsApp group)
- Submit only the tasks (2 or 3) before the deadline.
- Technical domain -> paste the GitHub repository links (public, working).
- Enter the CORRECT Student ID.
- Review everything, then click Submit once (no duplicate submissions).

## GitHub "About" text
- Task 1: Language Translation Tool - translate text between 100+ languages with Streamlit and Google Translate. CodeAlpha AI Internship.
- Task 2: FAQ chatbot using NLTK, TF-IDF and cosine similarity with a Streamlit chat UI. CodeAlpha AI Internship.
- Task 4: Real-time object detection and tracking with YOLOv8, ByteTrack and OpenCV. CodeAlpha AI Internship.
Topics: python, ai, codealpha, internship, nlp / computer-vision, streamlit, yolo, opencv
