import streamlit as st
import pandas as pd
from mongoDB_handler import MongoDBHandler
from streamlit_utils import display_dataframe_with_selections


st.set_page_config(
    page_title="News Catalog",
    page_icon=":book:",
    layout="centered",  # centered/wide
)

st.title(":book: News Catalog")

settings = st.secrets["mongo"]
mongodb = MongoDBHandler(mongoDB_settings=settings)
items = mongodb.get_data()

df = pd.DataFrame(items, index=list(range(len(items))))

column_config = {
    "_id": None,
    "title": "Title",
    "date": st.column_config.DateColumn("Date"),
    "lead": None,
    "text": None,
    "author": "Author",
    "url": None,
    "Read": st.column_config.CheckboxColumn(required=True),
}

selected_articles = display_dataframe_with_selections(df, column_config)

for article in selected_articles.values():
    st.header(article["title"])
    st.caption(f"{article['author']}, {article['date']}")
    st.write(article["lead"])
    st.write(article["text"])
