import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Information Retrieval", layout="wide")

st.title("📚 Dashboard Information Retrieval")

try:
    df = pd.read_json("data/books.json")
except:
    try:
        df = pd.read_json("books.json")
    except Exception as e:
        st.error(f"Gagal membaca books.json\n\n{e}")
        st.stop()

st.success(f"Jumlah data: {len(df)}")

st.dataframe(df, use_container_width=True)

st.subheader("Statistik Data")
st.write(df.describe(include="all"))
