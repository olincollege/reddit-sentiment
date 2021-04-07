"""
Unit tests for sentiment_analysis.py
"""
import pytest
import pandas as pd

from sentiment_analysis import (
    find_replies,
    create_reply_dict,
    get_most_replied_comments,
    analyze_sentiment,
    avg_depth_sentiment,
    get_sentiment_by_depth
)

# Read in data.
df = pd.read_csv('./cleaneddata/AmItheAsshole_comments_cleaned.csv')

# Create testing DataFrame.
test_data = {
    'comment_id': ["1", "2a", "2b", "3a", "3b", "3c", "4a"],
    'comment_parent_id': ["0", "1", "1", "2a", "2a", "2b", "3a"],
    'tokenized_comment': ["comment 1a AWESOME", "comment 2a AWESOME",
                          "comment 2b TERRIBLE", "comment 3a AWESOME", "comment 3b TERRIBLE",
                          "comment 3c AWESOME", "comment 4a AWESOME"]
}
test_comment_df = pd.DataFrame.from_dict(test_data)

test_comments_by_depth = {0: ["1"], 1: ["2a", "2b"], 2: ["3a", "3b", "3c"],
                          3: ["4a"]}

test_reply_dicts = {0: ["1"], 1: ["2a", "2b"], 2: ["3a", "3b"], 3: ["4a"]}

# Define sets of test cases.

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
    (["today"], "neutral"),
    # Check that multiple neutral words return 0.
    (["today", "today"], "neutral"),
    # Check that a positive word is positive.
    (["acceptance"], "positive"),
    # Check that a negative word is negative.
    (["bad"], "negative"),
    # Check that positive words are positive.
    (["Woohoo!", "Almost done :)"], "positive"),
    # Check that negative words are negative.
    (["I did not have fun writing these unit tests", "I am sad"], "negative"),
    # Crowdsourced unit tests below!
]

get_avg_depth_sentiment_cases = [
    # Test a depth with one comment.
    (test_comment_df, 0, test_comments_by_depth, "positive"),
    # Test a depth with multiple comments.
    (test_comment_df, 2, test_comments_by_depth, "positive")
]

get_get_sentiment_by_depth_cases = [
    # Check that sentiment is mapped correctly.
    (test_comment_df, test_reply_dicts)
]

get_get_sentiment_lists_cases = [
    (test_comment_df, test_reply_dicts)
]

test_data = {
    'comment_id': ["1", "2a", "2b", "3a", "3b", "3c", "4a"],
    'comment_parent_id': ["0", "1", "1", "2a", "2a", "2b", "3a"],
    'tokenized_comment': ["comment 1a AWESOME", "comment 2a AWESOME",
                          "comment 2b TERRIBLE", "comment 3a AWESOME", "comment 3b TERRIBLE",
                          "comment 3c AWESOME", "comment 4a AWESOME"]
}
test_comment_df = pd.DataFrame.from_dict(test_data)

test_comments_by_depth = {0: ["1"], 1: ["2a", "2b"], 2: ["3a", "3b", "3c"],
                          3: ["4a"]}

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


@pytest.mark.parametrize("comment_df, depth, comments_by_depth, \
    expected_sentiment", get_avg_depth_sentiment_cases)
def test_avg_depth_sentiment(comment_df, depth, comments_by_depth,
                             expected_sentiment):
    """
    Test that average depth sentiment is returned correctly.

    Args:
        comment_df: DataFrame containing comment thread information.
        depth: An int representing the depth (nesting level) at which to
            average the reply sentiment scores.
        comments_by_depth: A dictionary representing the replies to a comment
        with the nesting depth as integer keys and lists of string comment ids
        as values.
    """
    if expected_sentiment == "positive":
        assert avg_depth_sentiment(comment_df, depth, comments_by_depth) > 0
    elif expected_sentiment == "negative":
        assert avg_depth_sentiment(comment_df, depth, comments_by_depth) < 0
    else:
        assert avg_depth_sentiment(comment_df, depth, comments_by_depth) == 0


@pytest.mark.parametrize("comment_df, reply_dicts")
def test_get_sentiment_by_depth(comment_df, reply_dicts):
    """
    Test that depth is correctly mapped to average comment sentiment.

    Args:
        comment_df: DataFrame containing cleaned comment data.
        reply_dicts: A list of dictionaries, where the key represents depth and
            the values represent the comment_id of each comment at that depth.
    """
    print(get_sentiment_by_depth(comment_df, reply_dicts))
    assert get_sentiment_by_depth(comment_df, reply_dicts) == 0
