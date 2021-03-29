"""
putting this here so pylint stops yelling at us
"""
from collections import defaultdict
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

"""
Analyze the sentiment of a subreddit.

Args:
    subreddit: String representing name of subreddit

Returns:
    TBD - 2-column dataframe or table for plotting
    column 0 = reply depth (int)
    column 1 = average sentiment for that depth
"""
def analyze_subreddit(subreddit):

    """
    Find all child replies to a comment.

    Args:
        df: DataFrame containing, at minimum, comment_id and comment_parent_id
            data.
        comment_id: String representing comment_id for the parent comment.

    Returns:
        List of strings containing comment_id values for child replies.
    """
    def find_replies(df, comment_id):
        return df['comment_id'][df['comment_parent_id'].str.contains(
                                                comment_id)].tolist()

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
    def create_depth_dict(depth, comment_id_of_parent):
        replies = find_replies(sub_df, comment_id_of_parent)
        if len(replies) == 0:
            return
        comments_by_depth[depth] += replies
        for reply_id in replies:
            create_depth_dict(depth + 1, reply_id)

    # Read in cleaned subreddit DataFrame
    sub_df = pd.read_csv('./cleaneddata/' + subreddit + '_comments_cleaned.csv')
    
    top_level_comments = ['f0wgu81']
    # top_level_comments = sub_df['comment_id'][sub_df['comment_parent_id'].str.contains(
    #                   sub_df['comment_parent_id'][0])].tolist()

    for comment in top_level_comments:
        comments_by_depth = defaultdict(list)
        create_depth_dict(1, comment)

    print(dict(comments_by_depth))
