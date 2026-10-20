"""Core translation logic for the Language Translation Tool.

Uses the Google Translate service through the `deep-translator` package
(no API key needed). Text-to-speech uses gTTS.
"""
import io

from deep_translator import GoogleTranslator

MAX_CHARS = 5000  # Google Translate per-request limit


def get_languages():
    """Return {language name: code}, e.g. {'english': 'en', 'hindi': 'hi'}."""
    return GoogleTranslator().get_supported_languages(as_dict=True)


def translate_text(text, source="auto", target="en"):
    """Translate `text` from `source` to `target` (language codes).

    Raises ValueError for empty / too long input and RuntimeError when the
    translation service cannot be reached.
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Please enter some text to translate.")
    if len(text) > MAX_CHARS:
        raise ValueError(f"Text is too long ({len(text)} chars). Limit is {MAX_CHARS}.")
    if source == target:
        return text
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as err:  # network errors, service errors, etc.
        raise RuntimeError(f"Translation failed: {err}") from err


def text_to_speech(text, lang="en"):
    """Return MP3 bytes of `text` spoken in `lang` (None if unsupported)."""
    from gtts import gTTS
    from gtts.lang import tts_langs

    if lang not in tts_langs():
        return None
    buffer = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buffer)
    return buffer.getvalue()
