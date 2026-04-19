import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Setup Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page config
st.set_page_config(page_title="📝 AI Text Summarizer", layout="centered")
st.title("📝 AI Text Summarizer")
st.write("Paste any article or long text and get an instant AI summary!")

# Settings
st.markdown("### ⚙️ Settings")
length = st.radio("Summary Length", ["Short", "Medium", "Long"], horizontal=True)

length_map = {
    "Short":  "in 2-3 sentences",
    "Medium": "in 1 short paragraph (5-6 sentences)",
    "Long":   "in 2-3 detailed paragraphs",
}
summary_instruction = length_map[length]

# Text input
st.markdown("### 📄 Input Text")
text = st.text_area("Paste your article or text here:", height=300,
                    placeholder="Paste any news article, blog post, or long text here...")

# Summarize button
if st.button("✨ Summarize", use_container_width=True):
    if not text.strip():
        st.warning("Please paste some text first!")
    elif len(text.split()) < 30:
        st.warning("Text is too short! Please paste a longer text.")
    else:
        with st.spinner("Summarizing..."):
            prompt = f"""Please summarize the following text {summary_instruction}.
Only return the summary, nothing else.

Text:
{text}"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response.choices[0].message.content

        st.markdown("### 💬 Summary")
        st.success(summary)

        # Word count stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Original Words", len(text.split()))
        col2.metric("Summary Words", len(summary.split()))
        col3.metric("Reduced By", f"{round((1 - len(summary.split()) / len(text.split())) * 100)}%")