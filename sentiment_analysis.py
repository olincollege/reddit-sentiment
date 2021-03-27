from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


def find_replies(df, comment_id):
    return df[df['comment_parent_id'] == comment_id]