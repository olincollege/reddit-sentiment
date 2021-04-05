"""
Unit tests for data_cleaning.py
"""
import pytest

from data_cleaning import (
    clean_comment,
    lemmatize_sentence
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

get_lemmatized_sentence_cases = [
    # Check that lemmatizing an empty string returns an empty strong.
    ("", ""),
    # Check that lemmatized words remain the same.
    ("frog", "frog"),
    # Check that lemmatized sentences remain the same.
    ("frog cake bake time", "frog cake bake time"),
    # Check that words are lemmatized.
    ("notebooks", "notebook"),
    # Check that sentences are lemmatized.
    ("the laws of physics", "the law of physic")
]

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.


@pytest.mark.parametrize("raw_comment, cleaned_comment", 
                         get_clean_comment_cases)
def test_clean_comment(raw_comment, cleaned_comment):
    """
    Test that comments are processed correctly.

    Args:
        raw_comment: A string representing a Reddit comment.
        cleaned_comment: A string representing a cleaned, tokenized, and 
            lemmatized Reddit comment.
    """
    assert clean_comment(raw_comment) == cleaned_comment

@pytest.mark.parametrize("comment, lemmatized_comment", 
                         get_lemmatized_sentence_cases)
def test_lemmatize_sentnece(comment, lemmatized_comment):
    """
    Test that comments are correctly lemmatized.
    
    Args:
        comment: A string containing the text to be lemmatized.
        lemmatized_comment: A string representing the lemmatized comment.
    """
    assert lemmatize_sentence(comment) == lemmatized_comment