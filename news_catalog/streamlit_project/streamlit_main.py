import streamlit as st
from mongoDB_handler import mongoDB_handler
import pandas as pd


def dataframe_with_selections(df, config):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        column_config=config,
        hide_index=True,
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]

    # return dict of selected articles as {index: {col: val, col:val, ...}}
    return selected_rows.to_dict(orient="index")


st.set_page_config(
    page_title="News Catalog",
    page_icon=":book:",
    layout="centered",
)

st.title(":book: News Catalog")

settings = st.secrets["mongo"]
mongodb = mongoDB_handler(mongoDB_settings=settings)
items = mongodb.get_data()

df = pd.DataFrame(items, index=list(range(len(items))))

column_config = {
    "_id": None,
    "title": "Article title",
    "data": st.column_config.DateColumn(),
    "lead": None,
    "text": None,
    "author": "Author",
    "url": None,
    "Read": st.column_config.CheckboxColumn(required=True),
}

selected_articles = dataframe_with_selections(df, column_config)

for article in selected_articles.values():
    st.header(article["title"])
    st.caption(f"{article['author']}, {article['date']}")
    st.write(article["lead"])
    st.write(article["text"])
