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
        query (str): Query that will be used to filter df.
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
        query (str): Query that will be used to filter df.
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
        query (str): Query that will be used to filter df.
    """
    user_text_input = st_column.text_input(
        f"Substring or regex in {col.title()}",
    )
    query = None
    if user_text_input:
        df = df[df[col].astype(str).str.contains(user_text_input)]
        query = f"{col}.str.contains('{user_text_input}', case=False)"

    return query


def display_dataframe_with_selections(df, config):
    """Display Dataframe with column for selection and return selected rows.

    Args:
        df (pd.DataFrame): Dataframe to be displayed.
        config (dict): Config for dataframe display.

    Returns:
        selected_rows (dict): Slected rows: {index: {col: val, col:val, ...}}
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


def display_selected_articles(
    selected_articles, all_articles, mongo_db, assign_tags
):
    try:
        all_tags = list(all_articles.explode("tags")["tags"].unique())
        all_tags.remove(np.nan)
    except:
        all_tags = []

    for article in selected_articles.values():
        st.header(article["title"])
        st.caption(f"{article['author']}, {article['date']}")
        st.write(article["lead"])
        st.write(article["text"])

        article_tags = article.get("tags", "")
        if isinstance(article_tags, float):
            article_tags = []

        st.write(f"Tags: {article_tags}")

        if assign_tags:
            edit_tags(article, all_tags, article_tags, mongo_db)


def edit_tags(article, all_tags, article_tags, mongo_db):
    tags_to_choose = all_tags + article_tags
    standard_tags = st.multiselect(
        label="Remove current tags or add new tag from a list",
        options=tags_to_choose,
        default=article_tags,
        key=f"{article['_id']}_multiselect",
    )

    new_defined_tag = st.text_input(
        label="Define new tag", key=f"{article['_id']}_text_input"
    )

    if new_defined_tag and (new_defined_tag not in tags_to_choose):
        edited_tags = standard_tags + [new_defined_tag]
    else:
        edited_tags = standard_tags

    save_button = st.button(
        label="Save Tags",
        key=f"{article['_id']}_button",
    )

    if save_button:
        _update_tags(
            tags=edited_tags,
            mongo_db=mongo_db,
            article_id=ObjectId(article["_id"]),
        )


def _update_tags(mongo_db, article_id, tags):
    if isinstance(tags, list):
        mongo_db.update_item(article_id, "tags", tags)
