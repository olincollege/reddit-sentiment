"""
DON'T FORGET TO PUT IN THE LOGIN INFO
ALSO TAKE IT OUT AFTER FINISHING EDITING
"""
import praw
import pandas as pd


def scrape_reddit_comments(account_id, account_secret, subreddit_list):
    """
    Accesses an instance of Reddit and scrapes the comments from the top post
    of each subreddit in subreddit_list.

    Args:
        account_id: String representing the client ID used to access the Reddit
                    app.
        account_secret: String representing the client secret to access the
                        Reddit app.

    Returns:
        Does not return anything. However, it writes the comments data to CSV
        files.
    """
    # Access API
    reddit = praw.Reddit(client_id=account_id,      # Enter client ID
                         client_secret=account_secret,  # Enter client secret
                         user_agent='Comment Scraper by u/sentiment-analyses',
                         username='',
                         password='')

    for sub in subreddit_list:
        subreddit = reddit.subreddit(sub)

        # Create dictionary for all comments
        comments_dict = {
            'comment_id': [],
            'comment_parent_id': [],
            'comment_body': [],
            'comment_link_id': []
        }

        # Selects single top post of all time from subreddit
        for submission in subreddit.top(limit=1):
            submission.comments.replace_more()
            for comment in submission.comments.list():
                # Add comment information to dictionary
                comments_dict['comment_id'].append(comment.id)
                comments_dict['comment_parent_id'].append(comment.parent_id)
                comments_dict['comment_body'].append(comment.body)
                comments_dict['comment_link_id'].append(comment.link_id)

        # Create DataFrame from comments dictionary and save it to a CSV file
        post_comments = pd.DataFrame(comments_dict)
        post_comments.to_csv('./rawdata/' + sub + '_comments.csv')
