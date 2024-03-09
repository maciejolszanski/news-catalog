import pandas as pd
import numpy as np
from news_catalog.streamlit_project.streamlit_utils import (
    _convert_columns_to_datetime,
    get_all_unique_tags,
    get_article_tags,
    create_sorted_articles_df,
)


def test_convert_columns_to_datetime():
    input_dict = {
        "id": [1, 2, 3],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "x": ["a", "b", "c"],
    }

    input_df = pd.DataFrame.from_dict(input_dict)
    columns = list(input_df.columns)

    actual_output = _convert_columns_to_datetime(input_df, columns)

    assert pd.api.types.is_datetime64_any_dtype(actual_output.date)
    assert pd.api.types.is_integer_dtype(actual_output.id)
    assert pd.api.types.is_object_dtype(actual_output.x)


def test_get_all_unique_tags_with_nones():
    articles_dict = {
        "id": [1, 2, 3, 4],
        "tags": [np.nan, [np.nan, "tag1"], ["tag1", "tag2"], [None, "tag3"]],
    }

    articles_df = pd.DataFrame(articles_dict)
    actual_output = get_all_unique_tags(articles_df)

    assert actual_output == ["tag1", "tag2", "tag3"]


def test_get_all_unique_tags_wo_nones():
    articles_dict = {
        "id": [1, 2, 3, 4],
        "tags": [["tag1"], ["tag2"], ["tag1", "tag2"], ["tag1", "tag3"]],
    }

    articles_df = pd.DataFrame(articles_dict)

    actual_output = get_all_unique_tags(articles_df)

    assert actual_output == ["tag1", "tag2", "tag3"]


def test_get_article_tags():
    article = {"id": 1, "tags": ["tag1", "tag2", "tag3"]}

    actual_output = get_article_tags(article)

    assert actual_output == ["tag1", "tag2", "tag3"]


def test_create_sorted_articles_df_date_asc():
    items = [
        {"a": 5, "b": "x", "date": "2023-01-01"},
        {"a": 2, "b": "b", "date": "2023-01-03"},
        {"a": 4, "b": "a", "date": "2023-01-02"},
    ]

    expected_df = pd.DataFrame(
        [
            {"a": 5, "b": "x", "date": "2023-01-01"},
            {"a": 4, "b": "a", "date": "2023-01-02"},
            {"a": 2, "b": "b", "date": "2023-01-03"},
        ]
    )

    actual_df = create_sorted_articles_df(items, "date")

    assert pd.testing.assert_frame_equal(actual_df, expected_df) is None


def test_create_sorted_articles_df_int_desc():
    items = [
        {"a": 1, "b": "x", "date": "2023-01-01"},
        {"a": 2, "b": "b", "date": "2023-01-03"},
        {"a": 4, "b": "a", "date": "2023-01-02"},
    ]

    expected_df = pd.DataFrame(
        [
            {"a": 4, "b": "a", "date": "2023-01-02"},
            {"a": 2, "b": "b", "date": "2023-01-03"},
            {"a": 1, "b": "x", "date": "2023-01-01"},
        ]
    )

    actual_df = create_sorted_articles_df(items, "a", False)

    assert pd.testing.assert_frame_equal(actual_df, expected_df) is None
