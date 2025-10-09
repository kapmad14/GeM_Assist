import streamlit as st, pandas as pd, os

st.title("Upload / Update My Catalogue")
st.markdown("Accepts a CSV with columns: sku, description, hsn, min_price, max_price, states_deliverable")

uploaded = st.file_uploader("Choose CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    st.write("Preview (first 5 rows):")
    st.dataframe(df.head())
    if st.button("Save as my master"):
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/my_catalogue.csv", index=False)
        st.success("Saved to data/my_catalogue.csv")