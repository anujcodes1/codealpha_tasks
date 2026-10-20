"""FAQ Chatbot - Streamlit chat UI.  Run:  streamlit run app.py"""
import streamlit as st

from chatbot import FAQChatbot

st.set_page_config(page_title="ShopEasy FAQ Chatbot", page_icon="💬")
st.title("💬 ShopEasy FAQ Chatbot")
st.caption("CodeAlpha AI Internship - Task 2 · NLTK + TF-IDF + cosine similarity")


@st.cache_resource
def get_bot():
    return FAQChatbot()


bot = get_bot()

with st.sidebar:
    st.header("Try asking")
    for item in bot.faqs[:8]:
        st.markdown(f"- {item['question']}")
    show_debug = st.checkbox("Show matched FAQ & score", value=False)
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 Ask me anything about orders, delivery, returns or payments."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    answer, score, matched = bot.get_response(prompt)
    if show_debug and matched:
        answer += f"\n\n*Matched: \"{matched}\" · similarity {score:.2f}*"
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
