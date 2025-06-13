import streamlit as st
import pandas as pd
import psycopg2

# Ambil connection string dari Streamlit Secrets (pastikan sudah diisi di dashboard Streamlit Cloud)
DB_CONNECTION = st.secrets["SUPABASE_DB_CONNECTION"]

@st.cache_data(ttl=600)
def load_data():
    try:
        # Buka koneksi ke database
        conn = psycopg2.connect(DB_CONNECTION)
        
        # Query untuk mengambil data cuaca
        query = "SELECT city, date, temperature, humidity FROM weather_data ORDER BY date DESC;"
        
        # Gunakan pandas untuk membaca SQL query hasilnya ke dataframe
        df = pd.read_sql(query, conn)
        
        # Tutup koneksi setelah selesai
        conn.close()
        
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Kembalikan dataframe kosong kalau gagal

st.title("Dashboard Data Cuaca")

# Load data dari DB
df = load_data()

if df.empty:
    st.write("Data tidak tersedia.")
else:
    st.dataframe(df)
    
    # Visualisasi sederhana: line chart suhu dan kelembapan per tanggal
    df["date"] = pd.to_datetime(df["date"])  # Pastikan kolom date dalam format datetime
    df_sorted = df.sort_values("date")       # Urutkan berdasarkan tanggal
    
    # Set tanggal sebagai index untuk visualisasi
    st.line_chart(df_sorted.set_index("date")[["temperature", "humidity"]])
