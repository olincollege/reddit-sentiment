###
# DON'T FORGET TO PUT IN THE LOGIN INFO
# ALSO TAKE IT OUT AFTER FINISHING EDITING
###

import praw
import pandas as pd

# Access API
reddit = praw.Reddit(client_id="",
                    client_secret="",
                    user_agent="Comment Scraper by u/sentiment-analyses",
                    username="",
                    password="")

subreddit_list = ['AmItheAsshole']
for sub in subreddit_list:
    subreddit = reddit.subreddit(sub)

comments_dict = {
    "comment_id": [],
    "comment_parent_id": [],
    "comment_body": [],
    "comment_link_id": []
}

# Top 5 posts all-time
for submission in subreddit.top(limit=1):
    submission.comments.replace_more()
    for comment in submission.comments.list():
        comments_dict["comment_id"].append(comment.id)
        comments_dict["comment_parent_id"].append(comment.parent_id)
        comments_dict["comment_body"].append(comment.body)
        comments_dict["comment_link_id"].append(comment.link_id)

#print(comments_dict["comment_id"])