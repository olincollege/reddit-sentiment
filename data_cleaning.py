import pandas as pd
#import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji
import re
import en_core_web_sm
import spacy

#nltk.download('wordnet')

def find_replies(df, comment_id):
    return df[df['comment_parent_id'] == comment_id]

def clean_comment(comment):
    comment = emoji.get_emoji_regexp().sub(u'', comment)
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
    tokenized_comment = tokenizer.tokenize(comment)
    tokenized_comment = [word.lower() for word in tokenized_comment]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokenized_comment]
    return lemmatized_tokens

am_i_the_asshole = pd.read_csv('AmItheAsshole_comments_top1.csv')

am_i_the_asshole['tokenized_comment'] = am_i_the_asshole['comment_body'].apply(clean_comment)

print(am_i_the_asshole['tokenized_comment'].head())

am_i_the_asshole.to_csv('AmItheAsshole_comments_cleaned.csv')