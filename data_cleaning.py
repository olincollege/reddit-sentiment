"""
putting this here so pylint stops yelling at us
"""
import re
import pandas as pd
# import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji
import en_core_web_sm
import spacy

# nltk.download('wordnet')

# Create list of strings of subreddits to scrape
subreddit_list = ['AmItheAsshole', 'politics', 'MadeMeSmile', 'AskReddit',
                  'TalesFromRetail']

"""
Prepares (cleans, tokenizes, lemmatizes) a comment for sentiment analysis.

Args:
    comment: String containing text of comment.

Returns:
    lemmatized_tokens: List of strings containing prepared text of comment.
"""
def clean_comment(comment):
    comment = emoji.get_emoji_regexp().sub(u'', comment)
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
    tokenized_comment = tokenizer.tokenize(comment)
    tokenized_comment = [word.lower() for word in tokenized_comment]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word)
                         for word in tokenized_comment]
    return lemmatized_tokens

for subreddit in subreddit_list:
    subreddit_df = pd.read_csv('./rawdata/' + subreddit + '_comments.csv')
    # Adds cleaned comment to column 'tokenized_comment'.
    subreddit_df['tokenized_comment'] = \
        subreddit_df['comment_body'].apply(clean_comment)
    subreddit_df.to_csv('./cleaneddata/' + subreddit + '_comments_cleaned.csv')
