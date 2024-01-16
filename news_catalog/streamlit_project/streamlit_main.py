import streamlit as st
from mongoDB_handler import mongoDB_handler


st.title("Hello App")
settings = st.secrets["mongo"]

mongodb = mongoDB_handler(mongoDB_settings=settings)

if mongodb:
    st.write("MongoDB Connected")
