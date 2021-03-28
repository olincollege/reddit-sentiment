import pandas as pd
from collections import defaultdict
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def analyze_subreddit(subreddit):
    def find_replies(df, comment_id):
        return df['comment_id'][df['comment_parent_id'].str.contains(comment_id)].tolist()

    def create_depth_dict(level, comment_id_of_parent):
        replies = find_replies(sub_df, comment_id_of_parent)
        if len(replies) == 0:
            return
        comments_by_depth[level] += replies
        for reply_id in replies:
            create_depth_dict(level + 1, reply_id)

    sub_df = pd.read_csv('./cleaneddata/' + subreddit + '_comments_cleaned.csv')
    top_level_comments = ['f0wgu81']
    # top_level_comments = sub_df['comment_id'][sub_df['comment_parent_id'].str.contains(
    #                   sub_df['comment_parent_id'][0])].tolist()

    for comment in top_level_comments:
        comments_by_depth = defaultdict(list)
        create_depth_dict(1, comment)

    print(dict(comments_by_depth))
    