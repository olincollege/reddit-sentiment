"""
Pre-process data for sentiment analysis.
"""
import emoji
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer, sent_tokenize
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('punkt')


def clean_comment(comment):
    """
    Prepares (cleans, tokenizes, lemmatizes) a comment for sentiment analysis.

    Args:
        comment: String containing text of comment.

    Returns:
        lemmatized_tokens: A string containing the prepared text of comment
        with sentences separated by backslashes.
    """
    # Remove emojis from comment
    comment = emoji.get_emoji_regexp().sub(u'', comment)
    # Tokenize comment (split into list of words) and remove links
    tokenized_comment = sent_tokenize(comment)
    
    lemmatized_comment = [lemmatize_sentence(comment) for comment in 
                          tokenized_comment]
    
    return '\\'.join(lemmatized_comment)

def lemmatize_sentence(sentence):
    """
    Lemmatizes a sentence.
    
    Args:
        sentence: A string representing a tokenized sentence.
    
    Returns:
        A lemmatized sentence.
    """
    tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|http\S+')
    words = tokenizer.tokenize(sentence)
    # Make all words lowercase
    words = [word.lower() for word in words]
    # Lemmatize word to change them to the stem words
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word)
                         for word in words]
    return ' '.join(lemmatized_tokens)

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
