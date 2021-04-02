"""
putting this here so pylint stops yelling at us
"""
import reddit_scraper
import data_cleaning
import sentiment_analysis

# Enter the names of the subreddits to analyze as strings. We have provided
# a sample selection here.
subreddit_list = ['AmItheAsshole', 'politics', 'MadeMeSmile', 'AskReddit',
                  'TalesFromRetail']

# Enter client ID and secret.
#ACCOUNT_ID = ''  # Account ID for reddit app access
#ACCOUNT_SECRET = ''  # Account secret for reddit app access

# Scrape comments from the top post of each subreddit
#reddit_scraper.scrape_reddit_comments(ACCOUNT_ID, ACCOUNT_SECRET,
#                                    subreddit_list)

# Create and store new files with cleaned and tokenized comments
# data_cleaning.store_tokenized_data(subreddit_list)

sentiment_analysis.analyze_subreddit("AmItheAsshole")