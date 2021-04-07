"""
Contains all of the plotting helper functions used in the
reddit-sentiment-analysis notebook.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def sentiment_line(subreddit, sentiment_dicts):
    """
    Plot a line plot with depth on the x axis and sentiment on the y axis.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    for comment_dict in sentiment_dicts:
        sns.lineplot(x=comment_dict.keys(), y=[value[0] for value in
                                               comment_dict.values()])
    plt.xlabel('Comment depth')
    plt.ylabel('Average compound sentiment score')
    plt.title(f'r/{subreddit} Most Replied Comments\' Sentiment Analysis')
    plt.show()


def sentiment_bubble(subreddit, sentiment_dicts):
    """
    Plots a bubble plot with depth on the x axis and sentiment on the y axis,
    with bubble size as a function as number of comments.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    for comment_dict in sentiment_dicts:
        sns.scatterplot(x=comment_dict.keys(), y=[value[0] for value in
                                                  comment_dict.values()],
                        size=[value[1] for value in comment_dict.values()],
                        alpha=0.75, legend=False, sizes=(20, 2000))
    plt.xlabel('Comment depth')
    plt.ylabel('Average compound sentiment score')
    plt.title(f'r/{subreddit} Most Replied Comments\' Sentiment Analysis')
    plt.show()


def get_sentiment_difference(sentiment_dicts):
    """
    Return the difference between average sentiments of adjacent depths.

    Args:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.

    Returns:
        difference_dicts: A list of dictionaries where the keys are depths and
        the values are normalized differences in sentiment.
    """
    difference_dicts = []
    for comment_dict in sentiment_dicts:
        difference_dict = {key: (0, 0) for key in comment_dict.keys()}
        for key in difference_dict.keys():
            difference_dict[key] = (comment_dict[key][0] - comment_dict[0][0],
                                    comment_dict[key][1])
        difference_dicts.append(difference_dict)
    return difference_dicts


def sentiment_difference_line(subreddit, sentiment_dicts):
    """
    Plot a line plot with depth on the x axis and sentiment, normalized so the
    first comment's sentiment is 0, on the y axis.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    difference_dicts = get_sentiment_difference(sentiment_dicts)
    for difference_dict in difference_dicts:
        sns.lineplot(x=difference_dict.keys(), y=[value[0] for value in
                                                  difference_dict.values()])
    plt.xlabel('Comment depth')
    plt.ylabel('Average compound sentiment score change')
    plt.title(f'r/{subreddit} Most Replied Comments\' Sentiment Change ' +
              'Over Depth')
    plt.show()


def sentiment_difference_bubble(subreddit, sentiment_dicts):
    """
    Plot a bubble plot with depth on the x axis and sentiment, normalized so
    the first comment's sentiment is 0, on the y axis.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    difference_dicts = get_sentiment_difference(sentiment_dicts)
    for difference_dict in difference_dicts:
        sns.scatterplot(x=difference_dict.keys(), y=[value[0] for value in
                        difference_dict.values()], size=[value[1] for value in
                        difference_dict.values()], alpha=0.75, legend=False,
                        sizes=(20, 2000))
    plt.xlabel('Comment depth')
    plt.ylabel('Average compound sentiment score change')
    plt.title(f'r/{subreddit} Most Replied Comments\' Sentiment Change ' +
              'Over Depth')
    plt.show()


def get_sentiment_categorized(sentiment_dicts):
    """
    Categorize a list of sentiment_dicts into starting with a comment that has
    negative, neutral, or positive sentiment.

    Args:
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.

    Returns:
        categorized_dicts: A list of lists of dictionaries, where there is one
        list each for negative, neutral, and positive starting sentiment, and
        the keys of the dictionaries are depths and the values are differences
        in sentiment with the first comment normalized to zero.
    """
    categorized_dicts = [[], [], []]
    for comment_dict in sentiment_dicts:
        if comment_dict[0][0] < 0:
            categorized_dicts[0].append(comment_dict)
        elif comment_dict[0][0] > 0:
            categorized_dicts[2].append(comment_dict)
        else:
            categorized_dicts[1].append(comment_dict)
    categorized_dicts[0] = get_sentiment_difference(categorized_dicts[0])
    categorized_dicts[1] = get_sentiment_difference(categorized_dicts[1])
    categorized_dicts[2] = get_sentiment_difference(categorized_dicts[2])
    return categorized_dicts


def sentiment_categorized_line(subreddit, sentiment_dicts):
    """
    Plot line plots with depth on the x-axis and sentiment on the y-axis, with
    one plot each for comments that start with negative, neutral, and positive
    sentiment, with the first comment normalized to zero sentiment.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    categorized_dicts = get_sentiment_categorized(sentiment_dicts)
    fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    for categorized_dict in categorized_dicts[0]:
        axs[0].plot(categorized_dict.keys(), [value[0] for value in
                                              categorized_dict.values()])
    axs[0].set_title('Negative Top Level Comment')

    for categorized_dict in categorized_dicts[1]:
        axs[1].plot(categorized_dict.keys(), [value[0] for value in
                                              categorized_dict.values()])
    axs[1].set_title('Neutral Top Level Comment')

    for categorized_dict in categorized_dicts[2]:
        axs[2].plot(categorized_dict.keys(), [value[0] for value in
                                              categorized_dict.values()])
    axs[2].set_title('Positive Top Level Comment')

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False,
                    right=False)
    plt.grid(False)
    fig.suptitle(f'r/{subreddit} Reply Chain Sentiment Change Categorized by' +
                 ' Top Level Comment Polarity')
    plt.xlabel('Comment depth')
    plt.ylabel('Average sentiment score change')
    plt.show()


def sentiment_categorized_bubble(subreddit, sentiment_dicts):
    """
    Plot bubble plots with depth on the x-axis and sentiment on the y-axis,
    with one plot each for comments that start with negative, neutral, and
    positive sentiment, with the first comment normalized to zero sentiment.
    The size of the bubbles correspond to the number of comments at that depth
    for that thread.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dicts: A list of dictionaries where the keys are the
        nesting depths for the comment replies and the values are a tuple of
        the average compound sentiment scores for that depth and the number
        of comments in that depth.
    """
    categorized_dicts = get_sentiment_categorized(sentiment_dicts)
    fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    for categorized_dict in categorized_dicts[0]:
        sns.scatterplot(ax=axs[0], x=categorized_dict.keys(), y=[value[0] for
                            value in categorized_dict.values()], size=[value[1]
                        for value in categorized_dict.values()], alpha=0.75,
legend=False, sizes=(20, 2000))
    axs[0].set_title('Negative Top Level Comment')

    for categorized_dict in categorized_dicts[1]:
        sns.scatterplot(ax=axs[1], x=categorized_dict.keys(), y=[value[0] for
                    value in categorized_dict.values()], size=[value[1] for
                            value in categorized_dict.values()], alpha=0.75,
                        legend=False, sizes=(20, 2000))
    axs[1].set_title('Neutral Top Level Comment')

    for categorized_dict in categorized_dicts[2]:
        sns.scatterplot(ax=axs[2], x=categorized_dict.keys(), y=[value[0] for
                            value in categorized_dict.values()], size=[value[1]
                        for value in categorized_dict.values()], alpha=0.75,
                        legend=False, sizes=(20, 2000))
    axs[2].set_title('Positive Top Level Comment')

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False,
                    right=False)
    plt.grid(False)
    fig.suptitle(f'r/{subreddit} Reply Chain Sentiment Change Categorized by ' +
                 'Top Level Comment Polarity')
    plt.xlabel('Comment depth')
    plt.ylabel('Average sentiment score change')
    plt.show()


def sentiment_distribution_violin(subreddit, sentiment_dict):
    """
    Create violin plots where the x-axis is depth and the y-axis is the
    compound average sentiment score for that depth.

    Args:
        subreddit: A string representing the name of the subreddit.
        sentiment_dict: A dictionary where the keys are the nesting depths for
        the comment replies and the values are a tuple of the average compound
        sentiment scores for that depth and the number of comments in that
        depth.
    """
    comment_df = pd.DataFrame(columns=['depth', 'sentiment'])
    for depth in sentiment_dict.keys():
        for sentiment in sentiment_dict[depth]:
            comment_df = comment_df.append(pd.DataFrame({'depth': depth,
                                        'sentiment': sentiment}, index=[0]))

    sns.violinplot(x=comment_df['depth'], y=comment_df['sentiment'])
    plt.xlabel('Comment depth')
    plt.ylabel('Compound Sentiment Score')
    plt.title(f'r/{subreddit} Comment Thread Sentiment Distribution by Depth')
