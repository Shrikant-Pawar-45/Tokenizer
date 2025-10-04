import streamlit as st
import docx2txt
from PyPDF2 import PdfReader

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Tokenizer Model — Text to Number",
    page_icon="🔠",
    layout="wide"
)

# -------------------- CUSTOM STYLES --------------------
st.markdown("""
    <style>
    .main {
        background-color: var(--background-color);
    }
    h1, h2, h3 {
        color: var(--text-color);
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #1e40af;
        color: white;
    }
    .scroll-box {
        overflow-x: auto;
        white-space: nowrap;
        border: 2px solid var(--secondary-background-color);
        border-radius: 10px;
        background-color: var(--background-color);
        padding: 10px;
        font-family: monospace;
        font-size: 14px;
        color: var(--text-color);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("🔗 Custom Tokenizer Model")
st.subheader("Convert text into numeric tokens and decode them back in real time")

st.markdown("---")

# -------------------- TOKENIZER FUNCTIONS --------------------
def build_vocab_char(text):
    unique_chars = sorted(set(text))
    return {ch: idx + 1 for idx, ch in enumerate(unique_chars)}

def build_vocab_word(text):
    words = text.split()
    unique_words = sorted(set(words))
    return {word: idx + 1 for idx, word in enumerate(unique_words)}

def tokenize(text, vocab, level):
    if level == "Character-level":
        return [vocab[ch] for ch in text if ch in vocab]
    else:
        return [vocab[word] for word in text.split() if word in vocab]

def detokenize(tokens, vocab):
    reverse_vocab = {v: k for k, v in vocab.items()}
    if not tokens:
        return ""
    if isinstance(tokens[0], int):
        return ''.join([reverse_vocab[num] for num in tokens if num in reverse_vocab])
    else:
        return ' '.join([reverse_vocab[num] for num in tokens if num in reverse_vocab])

# -------------------- SIDEBAR SETTINGS --------------------
st.sidebar.header("⚙️ Tokenization Settings")

level = st.sidebar.radio("Select Tokenization Type", ["Character-level", "Word-level"])
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📂 Upload a file (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
st.sidebar.markdown("---")
st.sidebar.info("Or enter text manually below 👇")

# -------------------- TEXT INPUT --------------------
text_input = ""

if uploaded_file:
    file_type = uploaded_file.type
    if "pdf" in file_type:
        pdf_reader = PdfReader(uploaded_file)
        text_input = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
    elif "wordprocessingml" in file_type or uploaded_file.name.endswith(".docx"):
        text_input = docx2txt.process(uploaded_file)
    elif "text" in file_type or uploaded_file.name.endswith(".txt"):
        text_input = uploaded_file.read().decode("utf-8")
else:
    text_input = st.text_area("✍️ Enter your text here:", height=150, placeholder="Type or paste text...")

# -------------------- BUTTONS --------------------
colA, colB = st.columns(2)
convert_clicked = colA.button("Convert")
reset_clicked = colB.button("Reset")

if reset_clicked:
    st.experimental_rerun()

# -------------------- MAIN PROCESS --------------------
if convert_clicked:
    if text_input.strip():
        vocab = build_vocab_char(text_input) if level == "Character-level" else build_vocab_word(text_input)
        tokens = tokenize(text_input, vocab, level)
        decoded = detokenize(tokens, vocab)

        # ----------- RESULTS DISPLAY -----------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧩 Vocabulary Mapping")
            vocab_str = ", ".join([f"{repr(k)}: {v}" for k, v in vocab.items()])
            st.markdown(f'<div class="scroll-box">{vocab_str}</div>', unsafe_allow_html=True)

            st.markdown("### 🔢 Encoded Tokens")
            token_str = ", ".join(map(str, tokens))
            st.markdown(f'<div class="scroll-box">{token_str}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("### 🔁 Decoded Text")
            st.text_area("Decoded Output", value=decoded, height=250)
    else:
        st.warning("⚠️ Please upload a file or enter text before converting.")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("Developed with Shrikant  🚀")
