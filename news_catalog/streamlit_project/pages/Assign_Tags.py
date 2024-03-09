import streamlit as st
from mongoDB_handler import MongoDBHandler
from streamlit_utils import (
    display_selected_articles,
    navigate_articles,
    create_sorted_articles_df,
)


st.title(":label: Assign tags to articles")

settings = st.secrets["mongo"]
mongodb = MongoDBHandler(mongoDB_settings=settings)
items = mongodb.get_data()

all_articles = create_sorted_articles_df(items, "date", False)

articles_no_tags_df = all_articles[all_articles["tags"].isna()].reset_index()
articles_no_tags = articles_no_tags_df.to_dict(orient="index")
st.write(
    f"There is still {len(articles_no_tags_df)}/{len(all_articles)} "
    + "articles with no tags assigned. Keep working :wink:"
)

index = navigate_articles(articles_no_tags)

articles_no_tags_df.reset_index(inplace=True)
article = {index: all_articles.loc[index].to_dict()}


display_selected_articles(article, all_articles, mongodb, assign_tags=True)
