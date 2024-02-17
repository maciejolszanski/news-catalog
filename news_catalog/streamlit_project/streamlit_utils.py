import streamlit as st
import pandas as pd

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
    modify = st.checkbox("Add filters")

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
            _, right = st.columns((1, 20))

            if col in categorical_columns or df[col].nunique() < 10:
                query = _filter_categorical_column(df, col, right)
                if query:
                    queries.append(query)

            elif is_datetime64_any_dtype(df[col]):
                query = _filter_datetime_column(df, col, right)
                if query:
                    queries.append(query)
            else:
                query = _filter_text_columns(df, col, right)
                if query:
                    queries.append(query)

            if queries:
                final_query = " and ".join(queries)
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
    user_cat_input = st_column.multiselect(
        f"Values for {col}",
        df[col].unique(),
    )

    query = None
    if user_cat_input:
        query = f"{col} in {user_cat_input}"

    return query


def _filter_datetime_column(df, col, st_column):
    user_date_input = st_column.date_input(
        f"Values for {col}",
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
    user_text_input = st_column.text_input(
        f"Substring or regex in {col}",
    )
    query = None
    if user_text_input:
        df = df[df[col].astype(str).str.contains(user_text_input)]
        query = f"{col}.str.contains('{user_text_input}', case=False)"

    return query


def display_dataframe_with_selections(df, config):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    df_with_selections = filter_dataframe(
        df_with_selections,
        allowed_columns=["title", "date", "author"],
        categorical_columns=["author"],
    )

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
