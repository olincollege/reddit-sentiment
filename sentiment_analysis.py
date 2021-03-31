"""
putting this here so pylint stops yelling at us
"""
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
# import nltk
# nltk.download('vader_lexicon')


def analyze_subreddit(subreddit):
    """
    Analyze the sentiment of a subreddit.

    Args:
        subreddit: String representing name of subreddit

    Returns:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are the
        average compound sentiment scores for that depth.
    """
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

    def create_depth_dict(depth, comment_id_of_parent):
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
        replies = find_replies(sub_df, comment_id_of_parent)
        if len(replies) == 0:
            return
        comments_by_depth[depth] += replies
        for reply_id in replies:
            create_depth_dict(depth + 1, reply_id)

    def get_most_replied_comments(reply_dicts):
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
            comment_body: String representing the body text of the comment.

        Returns:
            A float representing the average compound polarity score for the
            comment.
        """
        sia = SIA()
        results = []

        for word in comment_body:
            pol_score = sia.polarity_scores(word)
            pol_score['words'] = word
            results.append(pol_score['compound'])

        return sum(results) / len(results)

    def avg_depth_sentiment(depth, comments_by_depth):
        """
        Return average sentiment of all comments of the same depth.

        Args:
            depth: An int representing the depth (nesting level) to average
            the reply sentiment scores at.
            comments_by_depth: A dictionary representing the replies to a
            comment with the nesting depth as the keys and lists of comment ids
            as values.

        Returns:
            A float representing the average compound sentiment score of
            the replies at the given depth level.
        """
        if len(comments_by_depth[depth]) > 0:
            comment_ids = comments_by_depth[depth]
            sentiments = [analyze_sentiment(sub_df['tokenized_comment'].values[
                sub_df['comment_id'] == comment_id][0].split(','))
                for comment_id in comment_ids]

        return sum(sentiments) / len(sentiments)  # * len(sentiments) weight

    def get_sentiment_dicts(reply_dicts):
        sentiment_dicts = []
        for comment_dict in reply_dicts:
            sentiment_dict = defaultdict(float)
            for depth in comment_dict.keys():
                sentiment_dict[depth] = avg_depth_sentiment(depth, comment_dict)
            sentiment_dicts.append(dict(sentiment_dict))
        return sentiment_dicts

    # Read in cleaned subreddit DataFrame
    sub_df = pd.read_csv('./cleaneddata/' + subreddit +
                         '_comments_cleaned.csv')

    # Find top level comments (comments are already in order by depth, so
    # the parent of the first comment is the original post)
    top_level_comments = sub_df['comment_id'][sub_df['comment_parent_id'].str
                            .contains(sub_df['comment_parent_id'][0])].tolist()
    reply_dicts = []

    # Create dictionaries for each top level comment with all of their
    # replies organized by depth.
    for comment in top_level_comments:
        comments_by_depth = defaultdict(list)
        comments_by_depth[0].append(comment)
        create_depth_dict(1, comment)
        reply_dicts.append(dict(comments_by_depth))

    reply_dicts = get_most_replied_comments(reply_dicts)
    
    return get_sentiment_dicts(reply_dicts)