# reddit-sentiment: Allison Li &amp; Berwin Lan's midterm project

This repository contains the necessary files to perform and visualize sentiment analysis on a subreddit's top comment. In this project, we scraped Reddit for comments, cleaned the data, and performed sentiment analysis on the data. The enclosed Jupyter Notebook contains our visualizations and interpretations.

# Getting started
Clone this repo to your machine and open `main.py`, which runs the files `reddit_scraper.py` and `data_cleaning.py` to create local raw and cleaned data files in the folders `rawdata` and `cleaneddata` respectively for the subreddits 'AmItheAsshole', 'politics', 'MadeMeSmile', 'AskReddit', and 'TalesFromRetail'. This list can be modified in order to generate data for subreddits of your choice. The functions in `plotting_functions.py` take `subreddit` (a string representing the name of the subreddit) and `sentiment_dicts` (a list of dictionaries where the keys are the nesting depths for the comment replies and the values are a tuple of the average compound sentiment scores for that depth and the number of comments in that depth). To generate your own `sentiment_dicts`, import from `sentiment_analysis.py` and run `sentiment_dicts = analyze_subreddit_by_depth(subreddit)` (or `analyze_subreddit_distribution(subreddit)` for the violin plots) and replace `subreddit` with your desired subreddit.

# Packages used
We use the [PRAW (Python Reddit API Wrapper)](https://pypi.org/project/praw "Allows for simple access to reddit's API.") to access the [Reddit API](https://www.reddit.com/wiki/api "Reddit API Access."). You will need to create your own instance of the API with the User ID and Secret in order to scrape and store your own data. The data is stored and accessed using [pandas](https://pandas.pydata.org/ "A data analysis tool") DataFrames. [VADER (Valence Aware Dictionary and sEntiment Reasoner)](https://github.com/cjhutto/vaderSentiment), which is incorported into [NLTK (Natural Language Toolkit)](https://www.nltk.org/ "A toolkit to work with human language data."), is used for sentiment analysis. Creating your own data sets from Reddit subreddits requires a client ID and secret to be entered in `main.py`, which can be obtained through [the Reddit API](https://www.reddit.com/wiki/api "Reddit API Access"). Otherwise, files from the subreddits r/AmItheAsshole, r/politics, r/MadeMeSmile, r/AskReddit, and r/TalesFromRetail are available for download in the folders `rawdata` and `cleaneddata`.

You will need to install the packages used in this project, which can be done by running the following command in Bash:

`$ pip install emoji nltk pandas praw`

# Citations
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media(ICWSM-14). Ann Arbor, MI, June 2014.
