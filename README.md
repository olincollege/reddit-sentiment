# reddit-sentiment: Allison Li &amp; Berwin Lan's midterm project

This repository contains the necessary files to perform and visualize sentiment analysis on a subreddit. In this project, we scraped Reddit for comments, cleaned the data, and performed sentiment analysis on the data. The enclosed Jupyter Notebook contains our visualizations.

# Getting started
Clone this repo to your machine and open `main.py`, which runs the files `reddit_scraper.py` and `data_cleaning.py` to create local raw and cleaned data files in the folders `rawdata` and `cleaneddata` respectively. Afterwards, run `sentiment_analysis.py` on each subreddit to obtain a dictionary mapping comment depth to average sentiment. Please refer to `reddit-sentiment-analysis.ipynb` for example visualizations.

# Packages used
We use the [PRAW(Python Reddit API Wrapper)](https://pypi.org/project/praw "Allows for simple access to reddit's API.") to access the [Reddit API](https://www.reddit.com/wiki/api "Reddit API Access."). [VADER(Valence Aware Dictionary and sEntiment Reasoner)](https://github.com/cjhutto/vaderSentiment), which is incorported into [NLTK(Natural Language Toolkit)](https://www.nltk.org/ "A toolkit to work with human language data."). Creating your own data sets from Reddit subreddits requires a client ID and secret to be entered in `main.py`, which can be obtained through [the Reddit API](https://www.reddit.com/wiki/api "Reddit API Access"). Otherwise, files from the subreddits r/AmItheAsshole, r/politics, r/MadeMeSmile, r/AskReddit, and r/TalesFromRetail are available for download in the folders `rawdata` and `cleaneddata`.

You will need to install the packages used in this project, which can be done by running the following command in Bash:

`$ pip install emoji nltk pandas praw`

# Citations
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media(ICWSM-14). Ann Arbor, MI, June 2014.
