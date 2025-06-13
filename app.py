import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

DB_CONNECTION = st.secrets["SUPABASE_DB_CONNECTION"]

@st.cache_data(ttl=600)
def load_data():
    try:
        engine = create_engine(DB_CONNECTION)
        query = "SELECT city, date, temperature, humidity FROM weather_data ORDER BY date DESC;"
        df = pd.read_sql(query, engine)

        # Bersihkan data: hapus satuan ' C' dan ' %', lalu convert ke numerik
        df['temperature'] = df['temperature'].str.replace(' C', '', regex=False)
        df['humidity'] = df['humidity'].str.replace(' %', '', regex=False)
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['temperature', 'humidity', 'date'])
        df = df.sort_values('date')
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
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Custom hovertemplate untuk temperature
    hover_temp = (
        "<b>%{customdata[0]}</b><br>" +  # city
        "Date: %{x|%Y-%m-%d}<br>" +
        "Temperature: %{y:.2f} °C<br>" +
        "<extra></extra>"  # hilangkan info trace default
    )
    # Custom hovertemplate untuk humidity
    hover_hum = (
        "<b>%{customdata[0]}</b><br>" +
        "Date: %{x|%Y-%m-%d}<br>" +
        "Humidity: %{y:.0f} %<br>" +
        "<extra></extra>"
    )

    # Temperatur
    fig_temp = px.line(df, x='date', y='temperature', color='city',
                       labels={'temperature': 'Temperature (°C)', 'date': 'Date', 'city': 'City'},
                       title='Temperature per City Over Time',
                       custom_data=['city'])
    fig_temp.update_traces(hovertemplate=hover_temp)
    st.plotly_chart(fig_temp, use_container_width=True)

    # Humidity
    fig_hum = px.line(df, x='date', y='humidity', color='city',
                      labels={'humidity': 'Humidity (%)', 'date': 'Date', 'city': 'City'},
                      title='Humidity per City Over Time',
                      custom_data=['city'])
    fig_hum.update_traces(hovertemplate=hover_hum)
    st.plotly_chart(fig_hum, use_container_width=True)
