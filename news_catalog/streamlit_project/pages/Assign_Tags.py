import streamlit as st
import pandas as pd
from mongoDB_handler import MongoDBHandler
from streamlit_utils import (
    display_selected_articles,
)


def iterate_index(value):
    st.session_state.article_index += value


st.title("Assign tags for articles that have no tags")

settings = st.secrets["mongo"]
mongodb = MongoDBHandler(mongoDB_settings=settings)
items = mongodb.get_data()

articles = pd.DataFrame(items, index=list(range(len(items))))
articles_no_tags_df = articles[articles["tags"].isna()]
articles_no_tags = articles_no_tags_df.to_dict(orient="index")

if "article_index" not in st.session_state:
    st.session_state.article_index = min(articles_no_tags)

index = st.session_state.article_index

first_article = {index: articles_no_tags.get(index)}

st.write(
    f"There is still {len(articles_no_tags_df)}/{len(articles)} "
    + "articles with no tags assigned left.... Keep working :wink:"
)

left, _, right = st.columns([0.1, 1, 0.1])
right.button(":arrow_forward:", on_click=iterate_index, args=[1])
left.button(":arrow_backward:", on_click=iterate_index, args=[-1])


display_selected_articles(first_article, articles, mongodb, assign_tags=True)
