from spellchecker import SpellChecker
import streamlit as st

# Initialize spellchecker
spell = SpellChecker()


def correct_text(text):
    """Detects and corrects spelling errors in a given string."""
    if not text.strip():
        return "", []

    words = text.split()
    corrected_words = []
    corrections = []

    for word in words:
        # Strip non-alphanumeric characters for clean checking
        clean_word = "".join(filter(str.isalnum, word))

        if clean_word and clean_word.lower() in spell.unknown([clean_word]):
            # Find the best replacement candidate
            correction = spell.correction(clean_word.lower())
            if correction:
                # Retain original case (Capitalized or Uppercase)
                if clean_word.istitle():
                    correction = correction.title()
                elif clean_word.isupper():
                    correction = correction.upper()

                # Preserve surrounding punctuation
                corrected_word = word.replace(clean_word, correction)
                corrections.append((clean_word, correction))
            else:
                corrected_word = word
        else:
            corrected_word = word

        corrected_words.append(corrected_word)

    return " ".join(corrected_words), corrections


# Streamlit UI Setup
st.set_page_config(
    page_title="AI Autocorrect Tool", page_icon="📝", layout="centered"
)

st.title("📝 AI Autocorrect Tool")
st.write(
    "Detect and automatically correct textual and spelling errors in real-time."
)

# Text area input
user_input = st.text_area(
    "Enter sentence or text:",
    value="Thiss is a simple project to test autokorrect and text error detection.",
    height=120,
)

if st.button("Detect & Correct", type="primary"):
    corrected_output, corrections_list = correct_text(user_input)

    st.subheader("Corrected Text:")
    st.success(corrected_output)

    if corrections_list:
        st.subheader("Detected Corrections:")
        for original, corrected in corrections_list:
            st.write(f"- ❌ `{original}` ➡️ ✅ **{corrected}**")
    else:
        st.info("No spelling errors detected in your input.")
