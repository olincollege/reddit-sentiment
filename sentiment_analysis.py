"""
Analyze sentiment of a comment forest.
"""
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
import nltk
nltk.download('vader_lexicon')


def find_replies(comment_df, comment_id):
    """
    Find all child replies to a comment.

    Args:
        comment_df: DataFrame containing, at minimum, comment_id and
            comment_parent_id data.
        comment_id: String representing comment_id for the parent comment.

    Returns:
        List of strings containing comment_id values for child replies.
    """
    return comment_df['comment_id'][comment_df['comment_parent_id'].str
                                    .contains(comment_id)].tolist()


def create_reply_dict(comment_df, comment):
    """
    Organize comments by depth.

    Args:
        comment_df: DataFrame containing, at minimum, comment_id and
            comment_parent_id data.
        comment: A string representing the cleaned contents of the parent comment.

    Returns:
        comments_by_depth: A dictionary where the keys are depths and the
            values are lists of strings containing the comment texts at that
            depth.
    """
    comments_by_depth = defaultdict(list)
    comments_by_depth[0].append(comment)

    def build_depth_dict(depth, comment_id_of_parent):
        """
        For a comment and all its child comments, map each comment to its depth.

        Args:
            depth: Integer representing the depth of the comment, with the
                highest-level comment having depth = 1.
            comment_id_of_parent: String representing comment_id for the parent
                                comment.

        Assumptions:
            There exists a dictionary with integer keys and list values.
            This function is called within the scope of that dictionary.
        """
        replies = find_replies(comment_df, comment_id_of_parent)
        if len(replies) == 0:
            return
        comments_by_depth[depth] += replies
        for reply_id in replies:
            build_depth_dict(depth + 1, reply_id)

    build_depth_dict(1, comment)
    return dict(comments_by_depth)


def get_most_replied_comments(reply_dicts):
    """
    Get the most replied-to comments.

    Args:
        reply_dicts: A list of dictionaries, where the key represents depth and
            the values represent the comment_id of each comment at that depth.

    Returns:
        A list of comment_dict(s) for the comment(s) with the greatest number
            of replies.
    """
    max_depth = 0
    for comment_dict in reply_dicts:
        if max(comment_dict.keys()) > max_depth:
            max_depth = max(comment_dict.keys())

    return [comment_dict for comment_dict in reply_dicts if
            max(comment_dict.keys()) == max_depth]


def analyze_sentiment(comment_body):
    """
    Calculate the average sentiment of one comment's body text.

    The function calculates the compound polarity score using VADER for each
    word in the comment text and finds the average score for the comment.

    Args:
        comment_body: List of strings representing the text of the comment.

    Returns:
        A float representing the average compound polarity score for the
        comment.
    """
    sia = SIA()
    results = []

    for sentence in comment_body:
        pol_score = sia.polarity_scores(sentence)
        results.append(pol_score['compound'])

    try:
        return sum(results) / len(results)
    except ZeroDivisionError:
        return 0


def avg_depth_sentiment(comment_df, depth, comments_by_depth):
    """
    Return average sentiment of all comments of the same depth.

    Args:
        comment_df: DataFrame containing comment thread information.
        depth: An int representing the depth (nesting level) at which to
            average the reply sentiment scores.
        comments_by_depth: A dictionary representing the replies to a comment
        with the nesting depth as integer keys and lists of string comment ids
        as values.

    Returns:
        A float representing the average compound sentiment score of
        the replies at the given depth level.
    """
    if len(comments_by_depth[depth]) > 0:
        comment_ids = comments_by_depth[depth]

        sentiments = []
        for comment_id in comment_ids:
            try:
                tokenized_comment = comment_df['tokenized_comment'][comment_df[
                    'comment_id'] == comment_id].values[0].split('\\')
            # Catches invalid comments (NaN)
            except AttributeError:
                pass
            sentiments.append(analyze_sentiment(tokenized_comment))

    return sum(sentiments) / len(sentiments)


def get_sentiment_by_depth(comment_df, reply_dicts):
    """
    Map each depth to the average sentiment of the comments at that depth.

    Args:
        comment_df: DataFrame containing cleaned comment data.
        reply_dicts: A list of dictionaries, where the key represents depth and
            the values represent the text of each comment at that depth.

    Returns:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the float average compound sentiment scores for that depth and the
        integer number of comments in that depth.
    """
    sentiment_dicts = []
    for comment_dict in reply_dicts:
        sentiment_dict = defaultdict(float)
        for depth in comment_dict.keys():
            sentiment_dict[depth] = (avg_depth_sentiment(comment_df,
                                depth, comment_dict), len(comment_dict[depth]))
        sentiment_dicts.append(dict(sentiment_dict))
    return sentiment_dicts


def get_sentiment_lists(comment_df, reply_dicts):
    """
    Get lists of dictionaries mapping depth to comment sentiment.

    Args:
        comment_df: DataFrame containing cleaned comment data.
        reply_dicts: A list of dictionaries, where the key represents depth and
            the values represent the comment_id of each comment at that depth.

    Returns:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are floats
        representing the sentiment of comments at that depth.
    """
    sentiment_dicts = []
    for comment_dict in reply_dicts:
        sentiment_dict = defaultdict(list)
        for depth in comment_dict.keys():
            for comment_id in comment_dict[depth]:
                try:
                    comment = comment_df['tokenized_comment'][comment_df[
                        'comment_id'] == comment_id].values[0].split('\\')
                # Catches invalid comments (NaN)
                except AttributeError:
                    pass
                sentiment_dict[depth].append(analyze_sentiment(comment))
        sentiment_dicts.append(dict(sentiment_dict))
    return sentiment_dicts


def analyze_subreddit_by_depth(subreddit):
    """
    Analyze the sentiment of a subreddit.

    Args:
        subreddit: String representing name of subreddit

    Returns:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    # Read in cleaned subreddit DataFrame
    sub_df = pd.read_csv('./cleaneddata/' + subreddit +
                         '_comments_cleaned.csv')

    # Find top level comments (comments are already in order by depth, so
    # the parent of the first comment is the original post)
    top_level_comments = \
        sub_df['comment_id'][sub_df['comment_parent_id'].str.contains(sub_df[
            'comment_parent_id'][0])].tolist()

    # Create dictionaries for each top level comment with all of their
    # replies organized by depth.
    reply_dicts = [create_reply_dict(sub_df, comment) for comment in
                   top_level_comments]

    # Only use the comments with the deepest nesting of replies
    reply_dicts = get_most_replied_comments(reply_dicts)

    return get_sentiment_by_depth(sub_df, reply_dicts)


def analyze_subreddit_distribution(subreddit):
    """
    Analyze the distribution of sentiment scores.

    Args:
        subreddit: A string representing the subreddit name.

    Returns:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are floats
        representing the sentiment of comments at that depth.
    """
    # Read in cleaned subreddit DataFrame
    sub_df = pd.read_csv('./cleaneddata/' + subreddit +
                         '_comments_cleaned.csv')

    # Find top level comments (comments are already in order by depth, so
    # the parent of the first comment is the original post)
    top_level_comments = \
        sub_df['comment_id'][sub_df['comment_parent_id'].str.contains(sub_df[
            'comment_parent_id'][0])].tolist()

    # Create dictionaries for each top level comment with all of their
    # replies organized by depth.
    reply_dicts = [create_reply_dict(sub_df, comment) for comment in
                   top_level_comments]

    # Only use the comments with the deepest nesting of replies
    reply_dicts = get_most_replied_comments(reply_dicts)

    return get_sentiment_lists(sub_df, reply_dicts)
