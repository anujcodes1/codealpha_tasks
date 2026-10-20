"""Language Translation Tool - Streamlit UI.  Run:  streamlit run app.py"""
import streamlit as st

from translator import get_languages, text_to_speech, translate_text, MAX_CHARS

st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="centered")
st.title("🌐 Language Translation Tool")
st.caption("CodeAlpha AI Internship - Task 1")


@st.cache_data
def load_languages():
    return get_languages()


languages = load_languages()  # {'english': 'en', ...}
names = sorted(languages)

col1, col2, col3 = st.columns([5, 1, 5])
with col1:
    src_options = ["auto-detect"] + names
    src_name = st.selectbox("From", src_options, index=0)
with col2:
    st.markdown("<div style='text-align:center;padding-top:2rem;font-size:1.5rem'>➜</div>",
                unsafe_allow_html=True)
with col3:
    tgt_name = st.selectbox("To", names, index=names.index("hindi") if "hindi" in names else 0)

text = st.text_area("Enter text", height=160, max_chars=MAX_CHARS,
                    placeholder="Type or paste the text you want to translate...")

if st.button("Translate", type="primary", use_container_width=True):
    source = "auto" if src_name == "auto-detect" else languages[src_name]
    target = languages[tgt_name]
    try:
        with st.spinner("Translating..."):
            result = translate_text(text, source, target)
        st.session_state["result"] = result
        st.session_state["target"] = target
    except (ValueError, RuntimeError) as err:
        st.session_state.pop("result", None)
        st.error(str(err))

if "result" in st.session_state:
    st.subheader("Translation")
    # st.code shows a built-in copy button in its top-right corner
    st.code(st.session_state["result"], language=None, wrap_lines=True)
    if st.button("🔊 Listen"):
        try:
            audio = text_to_speech(st.session_state["result"], st.session_state["target"])
            if audio:
                st.audio(audio, format="audio/mp3", autoplay=True)
            else:
                st.warning("Text-to-speech is not available for this language.")
        except Exception as err:
            st.warning(f"Could not generate audio: {err}")
