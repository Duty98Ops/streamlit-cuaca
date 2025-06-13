import streamlit as st
import pandas as pd
import psycopg2

# Ambil connection string dari secrets (bukan .env)
DB_CONNECTION = st.secrets["SUPABASE_DB_CONNECTION"]

@st.cache_data(ttl=600)
def load_data():
    try:
        conn = psycopg2.connect(DB_CONNECTION)
        query = "SELECT city, date, temperature, humidity FROM weather_data ORDER BY date DESC;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

st.title("Dashboard Data Cuaca")

df = load_data()

if df.empty:
    st.write("Data tidak tersedia.")
else:
    st.dataframe(df)
    # Contoh visualisasi sederhana
    st.line_chart(df.set_index("date")[["temperature", "humidity"]])
