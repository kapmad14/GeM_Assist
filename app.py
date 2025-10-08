import streamlit as st
import openai
import os, tempfile

# load key from local file or cloud secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("GeM Tender Assist – Step 1")
uploaded = st.file_uploader("Drop GeM tender PDF", type="pdf")
if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        pdf_text = f.read()

        # keep only first 12 000 characters (≈ 30 pages)
    short_text = pdf_text.decode("utf-8", errors="ignore")[:12000]
    prompt = (
        "You are a JSON extractor. Return ONLY the following JSON, no extra words:\n"
        '{"buyer_name":"...","delivery_state":"...","bid_deadline":"YYYY-MM-DD","products":[{"description":"...","quantity":number,"uom":"..."}]}'
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt + "\n\n" + short_text}],
        temperature=0,
        response_format={"type": "json_object"}  # JSON mode
)


    st.json(response.choices[0].message.content)
    os.remove(tmp_path)