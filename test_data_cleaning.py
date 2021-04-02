"""
Unit tests for data_cleaning.py
"""
from collections import Counter
import pytest

from data_cleaning import (
    clean_comment,
)

# Define sets of test cases.

get_clean_comment_cases = [
    # Check that cleaning an empty string returns an empty string.
    ("", ""),
    # Check that links are cleaned.
    ("https://softdes.olin.edu/", "http softdes olin edu"),
    # Check that emojis are cleaned.
    ("🤓this 🤓 CONTAINS 🤓 emojis", "this contains emojis"),
    # Check that words are lemmatized.
    ("Remember breaks corporations", "remember break corporation"),
    # Check that sentences are correctly tokenized.
    ("this is a sentence. this is another sentence",
     "this is a sentence\\this is another sentence")
]

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.


@pytest.mark.parametrize("raw_comment, cleaned_comment", get_clean_comment_cases)
def test_clean_comment(raw_comment, cleaned_comment):
    """
    Test that comments are processed correctly.

    Args:
        raw_comment: A string representing a Reddit comment.
        cleaned_comment: A string representing a cleaned, tokenized, and lemmatized Reddit comment.
    """
    assert clean_comment(raw_comment) == cleaned_comment
