import pandas as pd
#import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji
import re
import en_core_web_sm
import spacy

# nltk.download('wordnet')

subreddit_list = ['AmItheAsshole', 'politics', 'MadeMeSmile', 'AskReddit',
                  'TalesFromRetail']


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
    subreddit_df['tokenized_comment'] = \
        subreddit_df['comment_body'].apply(clean_comment)
    subreddit_df.to_csv('./cleaneddata/' + subreddit + '_comments_cleaned.csv')
