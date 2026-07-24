import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Book Crawler Dashboard", layout="wide")

st.title("📚 Book Crawler Dashboard")

df = pd.read_json("books.json")

st.success(f"Berhasil memuat {len(df)} data buku")

# Membersihkan harga
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("£", "", regex=False)
    .astype(float)
)

# Sidebar
st.sidebar.header("Filter")

rating = st.sidebar.multiselect(
    "Pilih Rating",
    sorted(df["rating"].unique()),
    default=sorted(df["rating"].unique())
)

availability = st.sidebar.multiselect(
    "Ketersediaan",
    sorted(df["availability"].unique()),
    default=sorted(df["availability"].unique())
)

filtered = df[
    (df["rating"].isin(rating)) &
    (df["availability"].isin(availability))
]

st.dataframe(filtered, use_container_width=True)

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Buku", len(filtered))
col2.metric("Harga Rata-rata", f"£{filtered['price'].mean():.2f}")
col3.metric("Harga Maksimum", f"£{filtered['price'].max():.2f}")

st.subheader("Distribusi Rating")

fig = px.histogram(
    filtered,
    x="rating",
    color="rating"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Distribusi Harga")

fig2 = px.histogram(
    filtered,
    x="price",
    nbins=20
)

st.plotly_chart(fig2, use_container_width=True)
