"""
Unit tests for sentiment_analysis.py
"""
import pytest
import pandas as pd

from sentiment_analysis import (
    find_replies,
    create_reply_dict,
    get_most_replied_comments,
    analyze_sentiment
)

# Define sets of test cases.
df = pd.read_csv('./cleaneddata/AmItheAsshole_comments_cleaned.csv')
get_find_replies_cases = [
    # Check that a parent ID returns the IDs for its child comments.
    (df, "f0wi2tm", ["f0wkhsk", "f0wmt6f", "f0wr5vh", "f0wrl8w", "f0wphmz",
                     "f0wotby", "f0wnrcm", "f0wm18i", "f0wraxb", "f0x2pnj",
                     "f0wrxvy", "f0wqan5", "f0wku10", "f0wr3mb", "f0wr39m",
                     "f0wiv2l", "f0wqxjz", "f0wu3zc", "f0wl5hl", "f0wvgs9",
                     "f0wsrwa", "f0x9d8o", "f0wqbk9", "f0wr6qx", "f0wool4",
                     "f0zhdut"])
]

get_create_reply_dict_cases = [
    
    # Check that a comment with no replies is mapped to zero.
    (df, " ".join(("“Late” is relative. And even besides that, it’s not",
                    "like I wasn’t aware that I found cute girls cute much",
                    "earlier. There’s a difference between children",
                    "noticing each other and having a concrete",
                    "understating of sexual mechanisms. Sounds like your",
                    "parents needed to supervise you closer.")), {0: 
                    [" ".join(("“Late” is relative. And even besides that,",
                             "it’s not like I wasn’t aware that I found",
                             "cute girls cute much earlier. There’s a",
                             "difference between children noticing each",
                             "other and having a concrete understating of",
                             "sexual mechanisms. Sounds like your parents",
                             "needed to supervise you closer."))]}),

    # Check that a top-level comment with replies is correctly mapped.
    (df, " ".join(("How is locking him in the impetus for that to occur? The",
                   "kid already had free reign of the house. The OP from that",
                   "thread said they just gave the kid games to play to keep",
                   "them busy. He was already free to roam around and get a",
                   "drink. At any point, he could have downed liquid",
                   "detergent, juggled with knives or stuck his head in the",
                   "toilet.")), {0: [" ".join(("How is locking him in the",
                    "impetus for that to occur? The kid already had free",
                    "reign of the house. The OP from that thread said they",
                    "just gave the kid games to play to keep them busy. He",
                    "was already free to roam around and get a drink. At any",
                    "point, he could have downed liquid detergent, juggled",
                    "with knives or stuck his head in the toilet."))]})
]

get_most_replied_comments_cases = [
    # Check that for a single comment, it is the most replied-to comment.
    ([{1: "only comment"}], [{1: "only comment"}]),
    # Check that for comments with the same number of replies, they are all
    # returned as the most replied-to comment.
    ([{1: "depth is 1"}, {1: "depth is also 1"}, {1: "depth is also 1"}], [{
        1: "depth is 1"}, {1: "depth is also 1"}, {1: "depth is also 1"}]),
    # Check that when comments differ in number of replies, the one with the
    # most comments is returned.
    ([{1: "depth is 1"}, {1: "first comment", 2: "whoa look replies!"}], [{
        1: "first comment", 2: "whoa look replies!"}])
]

get_analyze_sentiment_cases = [
    # Check that an empty string returns 0.
    ("", "neutral"),
    # Check that a neutral word returns 0.
    ("today", "neutral"),
    # Check that multiple neutral words return 0.
    ("today today", "neutral")
]

# make sure expected depth is equal to actual depth -- test keys/non-sentiment parts

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.

@pytest.mark.parametrize("comment_df, comment_id, child_reply_ids",
                         get_find_replies_cases)
def test_find_replies(comment_df, comment_id, child_reply_ids):
    """
    Test that replies are correctly found.

    Args:
        comment_df: DataFrame containing, at minimum, comment_id and
            comment_parent_id data.
        comment_id: String representing comment_id for the parent comment.
        child_reply_ids: List of strings of comment IDs for replies.
    """
    assert find_replies(comment_df, comment_id) == child_reply_ids


@pytest.mark.parametrize("comment_df, comment, comments_by_depth",
                         get_create_reply_dict_cases)
def test_create_reply_dict(comment_df, comment, comments_by_depth):
    """
    Test that create_reply_dict correctly maps depth to comments.

    Args:
        comment_df: DataFrame containing, at minimum, comment_id and
            comment_parent_id data.
        comment: A string representing the cleaned contents of the parent
            comment.
        comments_by_depth: A dictionary where the keys are depths and the
            values are lists of strings containing the comment texts at that
            depth.
    """
    assert create_reply_dict(comment_df, comment) == comments_by_depth


@pytest.mark.parametrize("reply_dicts, most_replied_comment",
                         get_most_replied_comments_cases)
def test_most_replied_comments(reply_dicts, most_replied_comment):
    """
    Test that the most replied-to functions are found and returned.

    Args:
        reply_dicts: A list of dictionaries, where the key represents depth and
            the values represent the comment_id of each comment at that depth.
        most_replied_comment: A list of comment_dict(s) for the comment(s) with
            the greatest number of replies.
    """
    assert get_most_replied_comments(reply_dicts) == most_replied_comment


@pytest.mark.parametrize("comment_body, expected_sentiment", 
                         get_analyze_sentiment_cases)
def test_analyze_sentiment(comment_body, expected_sentiment):
    """
    Test that sentiment analysis works as expected.

    Args:
        comment_body: A string representing the body text of the comment.
        expected_sentiment: A string representing the expected sentiment of the
            comment_body, being either positive, neutral, or negative.
    """
    if expected_sentiment == "positive":
        assert analyze_sentiment(comment_body) > 0
    elif expected_sentiment == "negative":
        assert analyze_sentiment(comment_body) < 0
    else:
        assert analyze_sentiment(comment_body) == 0
