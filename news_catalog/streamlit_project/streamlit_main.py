import streamlit as st
from mongoDB_handler import mongoDB_handler
import pandas as pd


st.title("News Catalog")
settings = st.secrets["mongo"]

mongodb = mongoDB_handler(mongoDB_settings=settings)

items = mongodb.get_data()
df = pd.DataFrame(items, index=list(range(len(items))))

# display without id
df.iloc[:, 1:]
