import streamlit as st
from mongoDB_handler import MongoDBHandler
from streamlit_utils import (
    display_dataframe_with_selections,
    display_selected_articles,
    create_sorted_articles_df,
)


st.set_page_config(
    page_title="News Catalog",
    page_icon=":book:",
    layout="wide",  # centered/wide
)

st.title(":book: News Catalog")

settings = st.secrets["mongo"]
mongodb = MongoDBHandler(mongoDB_settings=settings)
items = mongodb.get_data()

articles = create_sorted_articles_df(items, "date", False)

column_config = {
    "_id": None,
    "title": "Title",
    "date": st.column_config.DateColumn("Date"),
    "lead": None,
    "text": None,
    "author": "Author",
    "url": None,
    "tags": "Tags",
}

selected_articles = display_dataframe_with_selections(articles, column_config)

assign_tags = False
if selected_articles:
    assign_tags = st.toggle("Edit Tags Manually")

display_selected_articles(selected_articles, articles, mongodb, assign_tags)
