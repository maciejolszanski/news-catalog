import streamlit as st
import pandas as pd
from bson import ObjectId
import numpy as np

from pandas.api.types import (
    is_datetime64_any_dtype,
    is_object_dtype,
)


def filter_dataframe(df, allowed_columns, categorical_columns=[]):
    """Adds a UI on top of a dataframe to let viewers filter columns.

    Args:
        df (pd.DataFrame): Original dataframe.

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    modify = st.toggle("Filters")

    if not modify:
        return df

    df = df.copy()
    df = _convert_columns_to_datetime(df, allowed_columns)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect(
            "Filter dataframe on", allowed_columns
        )
        queries = []

        for col in to_filter_columns:
            _, right = st.columns([0.1, 0.9])

            if col in categorical_columns:
                query = _filter_categorical_column(df, col, right)
                queries.append(query)

            elif is_datetime64_any_dtype(df[col]):
                query = _filter_datetime_column(df, col, right)
                queries.append(query)

            else:
                query = _filter_text_columns(df, col, right)
                queries.append(query)

            queries_filtered = list(filter(lambda x: x is not None, queries))
            if queries_filtered:
                final_query = " and ".join(queries_filtered)
                df = df.query(final_query)

    return df


def _convert_columns_to_datetime(df, columns):
    """Convert to datetime "%Y-%m-%d" if column is a string formatted as date.

    Args:
        df (pd.DateFrame): Input dataframe.
        columns (list): List of columns name to be checked and coverted.
    """
    for col in columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")
            except ValueError:
                pass

    return df


def _filter_categorical_column(df, col, st_column):
    """Filter categorical column based on user input.

    Args:
        df (pd.DataFrame): Dataframe to be filtered.
        col (str): Column to be filtered.
        st_column (st.delta_generator.DeltaGenerator): Streamlit column.

    Returns:
        str: Query that will be used to filter df.
    """
    user_cat_input = st_column.multiselect(
        f"Values for {col.title()}",
        df[col].unique(),
    )

    query = None
    if user_cat_input:
        query = f"{col} in {user_cat_input}"

    return query


def _filter_datetime_column(df, col, st_column):
    """Filter datetime column based on user input.

    Args:
        df (pd.DataFrame): Dataframe to be filtered.
        col (str): Column to be filtered.
        st_column (st.delta_generator.DeltaGenerator): Streamlit column.

    Returns:
        str: Query that will be used to filter df.
    """
    user_date_input = st_column.date_input(
        f"Values for {col.title()}",
        value=(
            df[col].min(),
            df[col].max(),
        ),
    )

    query = None
    if len(user_date_input) == 2:
        start_date, end_date = user_date_input
        query = f"'{str(start_date)}' <= {col} <= '{str(end_date)}'"

    return query


def _filter_text_columns(df, col, st_column):
    """Filter text column based on user input.

    Args:
        df (pd.DataFrame): Dataframe to be filtered.
        col (str): Column to be filtered.
        st_column (st.delta_generator.DeltaGenerator): Streamlit column.

    Returns:
        str: Query that will be used to filter df.
    """
    user_text_input = st_column.text_input(
        f"Substring or regex in {col.title()}",
    )
    query = None
    if user_text_input:
        query = f"{col}.str.contains('{user_text_input}', case=False)"

    return query


def display_dataframe_with_selections(df, config):
    """Display Dataframe with column for selection and return selected rows.

    Args:
        df (pd.DataFrame): Dataframe to be displayed.
        config (dict): Config for dataframe display.

    Returns:
        dict: Slected rows: {index: {col: val, col:val, ...}}
    """
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Read", False)

    df_with_selections = filter_dataframe(
        df_with_selections,
        allowed_columns=["title", "date", "author"],
        categorical_columns=["author"],
    )

    edited_df = st.data_editor(
        df_with_selections,
        column_config=config,
        hide_index=True,
        disabled=df.columns,
    )

    selected_rows = edited_df[edited_df["Read"]]
    selected_rows = selected_rows.to_dict(orient="index")

    return selected_rows


def get_all_unique_tags(articles: pd.DataFrame) -> list:
    """Get unique list of tags from input dataframe."""

    disallowed_tags = [None, np.nan, "", float("nan"), []]

    all_tags = list(articles.explode("tags")["tags"].unique())

    for disallowed_tag in disallowed_tags:
        if disallowed_tag in all_tags:
            all_tags.remove(disallowed_tag)

    return all_tags


def get_article_tags(article: dict) -> list:
    """Get list of article tags."""
    article_tags = article.get("tags", [])
    if article_tags is None:
        article_tags = []

    return article_tags


def display_article_text(article: dict) -> None:
    """Display article as well formatted text."""
    st.header(article["title"])
    st.caption(f"{article['author']}, {article['date']}")
    st.write(article["lead"])
    st.write(article["text"])
    st.caption(f"Read the original article: {article['url']}")

    article_tags = get_article_tags(article)
    display_article_tags(article_tags)


def display_article_tags(article_tags: list) -> None:
    """Add hash to tags and display."""
    tags_with_hash = [f"#{tag}" for tag in article_tags]
    st.write(f"Tags: :red[{' '.join(tags_with_hash)}]")


def display_selected_articles(
    selected_articles, all_articles, mongo_db, assign_tags
):
    """Display article to be read and add possibility to assign tags.

    Args:
        selected_articles (dict): Dict {index: article_dict, ...}.
        all_articles (pd.DataFrame): DataFrame of all articles.
        mongo_db (MongoDBHandler): MongoDBHandler object.
        assign_tags (bool): If the UI for assigning tags should be enabled.
    """
    all_tags = get_all_unique_tags(all_articles)

    for article in selected_articles.values():
        display_article_text(article)

        if assign_tags:
            edit_tags(article, all_tags, get_article_tags(article), mongo_db)


def edit_tags(article, known_tags, article_tags, mongo_db):
    """Add or remove tags to article.

    Function displays multiselect field, text_input and button:
      - multiselect - displays currently assigned tags
      - text_input  - adds new tag that doesn't exist in multiselect option
                      and saves all chosen tags to mongodb.
      - button      - saves tags to mongo_db

    Args:
        article (dict): Article to assign tags for.
        known_tags (list): All known tags in DB.
        article_tags (list): Tags of selected article.
        mongo_db (MongoDBHandler): MongoDBHandler object.
    """

    if f"{article['_id']}_text_input" not in st.session_state:
        st.session_state[f"{article['_id']}_text_input"] = ""

    tags_to_choose = known_tags
    displayed_tags = article_tags

    assigned_tags = st.multiselect(
        label="Remove current tags or add new tag from a list "
        + ":red[(Remeber to save when done with editing)]",
        options=tags_to_choose,
        default=displayed_tags,
        key=f"{article['_id']}_multiselect",
    )

    kwargs_to_save_tags = {
        "tags": assigned_tags,
        "mongo_db": mongo_db,
        "article_id": article["_id"],
    }

    text_input_key = f"{article['_id']}_text_input"
    st.text_input(
        label="Define new tag",
        key=text_input_key,
        on_change=add_new_tag,
        kwargs={
            "text_input_key": text_input_key,
            **kwargs_to_save_tags,
        },
    )

    st.button(
        label="Save Tags",
        key=f"{article['_id']}_button",
        on_click=_update_tags,
        kwargs=kwargs_to_save_tags,
    )


def add_new_tag(text_input_key: str, **update_tags_kwargs) -> None:
    """Add tag to article by text input field and clear text input."""

    new_tags = []
    new_tag = st.session_state[text_input_key].lower()
    if new_tag != "":
        new_tags = [new_tag]

    tags_to_assign = update_tags_kwargs.get("tags", []) + new_tags
    update_tags_kwargs.update({"tags": tags_to_assign})

    _update_tags(**update_tags_kwargs)
    st.session_state[text_input_key] = ""


def _update_tags(mongo_db, article_id: str, tags: list):
    """Save tags selected in multiselect field to mongodb."""
    if isinstance(tags, list):
        mongo_db.update_item(ObjectId(article_id), "tags", tags)


def navigate_articles(articles: pd.DataFrame) -> int:
    """Iterate over articles based on their index.

    Args:
        articles (pd.DataFrame): DF containing articles to navigate between.

    Returns:
        int: Index of article to be displayed.
    """

    def _iterate_index(value):
        st.session_state.article_index += value

    if "article_index" not in st.session_state:
        st.session_state.article_index = 0

    articles_num = len(articles)
    index = st.session_state.article_index

    st.text(f"{index}/{articles_num}")

    left, _, right = st.columns([0.1, 1, 0.1])
    if index < articles_num:
        right.button(":arrow_forward:", on_click=_iterate_index, args=[1])
    if index > 0:
        left.button(":arrow_backward:", on_click=_iterate_index, args=[-1])

    return index


def create_sorted_articles_df(
    mongodb_items: list, column_name: str, ascending=True
) -> pd.DataFrame:
    """Create DataFrame sorted by date in descending order.

    Args:
        mongodb_items (list): List of MongoDB documents.
        column_name (str): Name of column to sort by.

    Returns:
        pd.DataFrame: Articles DataFrame sorted by date in descending order.
    """
    indices = list(range(len(mongodb_items)))
    all_articles = pd.DataFrame(mongodb_items, index=indices)
    all_articles_sorted = all_articles.sort_values(
        column_name, ascending=ascending
    )
    all_articles_sorted.reset_index(drop=True, inplace=True)

    return all_articles_sorted
