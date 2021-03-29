"""
DON'T FORGET TO PUT IN THE LOGIN INFO
ALSO TAKE IT OUT AFTER FINISHING EDITING
"""


import praw
import pandas as pd

# Access API
reddit = praw.Reddit(client_id='',      # Enter client ID
                     client_secret='',  # Enter client secret
                     user_agent='Comment Scraper by u/sentiment-analyses',
                     username='',
                     password='')

# Select subreddit(s) to scrape
subreddit_list = ['AmItheAsshole', 'politics', 'MadeMeSmile', 'AskReddit',
                  'TalesFromRetail']

for sub in subreddit_list:
    subreddit = reddit.subreddit(sub)

    # Choose types of data to save
    comments_dict = {
        'comment_id': [],
        'comment_parent_id': [],
        'comment_body': [],
        'comment_link_id': []
    }

    # Selects single top post of all time
    # limit = top n posts of all time
    for submission in subreddit.top(limit=1):
        submission.comments.replace_more()
        for comment in submission.comments.list():
            comments_dict['comment_id'].append(comment.id)
            comments_dict['comment_parent_id'].append(comment.parent_id)
            comments_dict['comment_body'].append(comment.body)
            comments_dict['comment_link_id'].append(comment.link_id)

    # Create DataFrame from comments dictionary and save it to a CSV file
    post_comments = pd.DataFrame(comments_dict)
    post_comments.to_csv('./rawdata/' + sub + '_comments.csv')
