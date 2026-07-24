from pathlib import Path
import streamlit as st
import pandas as pd

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Dashboard Information Retrieval",
    page_icon="📚",
    layout="wide"
)

# ==========================
# JUDUL
# ==========================
st.title("📚 Dashboard Information Retrieval")
st.markdown("### Hasil Crawling Data Buku")

# ==========================
# SIDEBAR
# ==========================
st.sidebar.title("📖 Informasi")

st.sidebar.markdown("### Identitas")
st.sidebar.write("**Nama :** ARIF RAHMAT RISKI")
st.sidebar.write("**NIM :** 24146092")
st.sidebar.write("**Mata Kuliah :** Information Retrieval")

st.sidebar.markdown("---")

# ==========================
# MEMBACA FILE JSON
# ==========================
BASE_DIR = Path(__file__).parent
json_file = BASE_DIR / "data" / "books.json"

try:
    df = pd.read_json(json_file)
except Exception as e:
    st.error(f"Gagal membaca books.json\n\n{e}")
    st.stop()

# ==========================
# MEMBERSIHKAN DATA HARGA
# ==========================
df["price"] = (
    df["price"]
    .str.replace("£", "", regex=False)
    .astype(float)
)

# ==========================
# FILTER RATING
# ==========================
rating = st.sidebar.selectbox(
    "Filter Rating",
    ["Semua"] + sorted(df["rating"].unique().tolist())
)

if rating != "Semua":
    df = df[df["rating"] == rating]

# ==========================
# PENCARIAN
# ==========================
search = st.text_input("🔍 Cari Judul Buku")

if search:
    df = df[df["title"].str.contains(search, case=False)]

# ==========================
# METRIC
# ==========================
col1, col2, col3 = st.columns(3)

col1.metric("📚 Jumlah Buku", len(df))
col2.metric("💷 Harga Rata-rata", f"£{df['price'].mean():.2f}")
col3.metric("⭐ Jumlah Rating", df["rating"].nunique())

st.markdown("---")

# ==========================
# GRAFIK
# ==========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Jumlah Buku Berdasarkan Rating")
    st.bar_chart(df["rating"].value_counts())

with col2:
    st.subheader("📦 Ketersediaan Buku")
    st.bar_chart(df["availability"].value_counts())

st.markdown("---")

# ==========================
# DATAFRAME
# ==========================
st.subheader("📋 Data Buku")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# STATISTIK
# ==========================
st.subheader("📈 Statistik Data")

st.write(df.describe())

st.markdown("---")

# ==========================
# DOWNLOAD CSV
# ==========================
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Data CSV",
    data=csv,
    file_name="books.csv",
    mime="text/csv",
)
