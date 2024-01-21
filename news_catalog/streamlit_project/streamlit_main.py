import streamlit as st
from mongoDB_handler import mongoDB_handler
import pandas as pd

st.set_page_config(layout="wide")

st.title("News Catalog")
settings = st.secrets["mongo"]

mongodb = mongoDB_handler(mongoDB_settings=settings)

items = mongodb.get_data()
df = pd.DataFrame(items, index=list(range(len(items))))

# display without id
column_config = {
    "_id": None,
    "title": "Article title",
    "data": st.column_config.DateColumn(),
    "lead": None,
    "text": None,
    "author": "Author",
    "url": None,
}

st.dataframe(df, column_config=column_config)
