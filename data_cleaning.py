"""
putting this here so pylint stops yelling at us
"""
import emoji
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import nltk
nltk.download('wordnet')


def clean_comment(comment):
    """
    Prepares (cleans, tokenizes, lemmatizes) a comment for sentiment analysis.

    Args:
        comment: String containing text of comment.

    Returns:
        lemmatized_tokens: A string containing the prepared text of comment
        with words separated by commas.
    """
    # Remove emojis from comment
    comment = emoji.get_emoji_regexp().sub(u'', comment)
    # Tokenize comment (split into list of words) and remove links
    tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|http\S+')
    tokenized_comment = tokenizer.tokenize(comment)
    # Make all words lowercase
    tokenized_comment = [word.lower() for word in tokenized_comment]
    # Lemmatize word to change them to the stem words
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word)
                         for word in tokenized_comment]
    return ','.join(lemmatized_tokens)


def store_tokenized_data(subreddit_list):
    """
    Creates new data files for each subreddit with the comment body texts
    stored in tokenized and lemmatized form.

    Args:
        subreddit_list: List of strings representing subreddits to store data
        for
    """
    for subreddit in subreddit_list:
        # Read the raw data for the subreddit from a CSV
        subreddit_df = pd.read_csv('./rawdata/' + subreddit + '_comments.csv')
        # Add cleaned comment to column 'tokenized_comment'.
        subreddit_df['tokenized_comment'] = \
            subreddit_df['comment_body'].apply(clean_comment)
        # Save the new dataframe with tokenized comments to a new CSV file
        subreddit_df.to_csv('./cleaneddata/' + subreddit +
                            '_comments_cleaned.csv')
