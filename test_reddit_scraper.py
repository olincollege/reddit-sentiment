"""
Unit tests for reddit_scraper.py
Make sure reddit_scraper.py has processed files before running.
"""
import pytest
import os.path

# Define sets of test cases.

subreddit_list = ['AmItheAsshole', 'politics', 'MadeMeSmile', 'AskReddit',
                  'TalesFromRetail']

get_scrape_reddit_comments_cases = [
    # Check that data is not stored in the wrong directory.
    ("punkt", subreddit_list, False),
    # Check that data is stored in the correct directory.
    ("rawdata", subreddit_list, True)
]


# Define standard testing functions to check functions' outputs given certain
# inputs defined above.

@pytest.mark.parametrize("directory, subreddit_list, expected_boolean", 
                         get_scrape_reddit_comments_cases)
def test_store_tokenized_data(directory, subreddit_list, expected_boolean):
    """
    Test that data is stored in the correct directory with the correct filename
    
    Args:
        directory: A string representing the directory name.
        subreddit_list: A list of strings representing the name of the
            subreddit whose data is being stored.
        expected_boolean: A Boolean value representing the expected outcome
            (True if a file should exist, False if not)
    """    
    for subreddit in subreddit_list:
        path = './' + directory + '/' + subreddit +'_comments.csv'
        print(path)
        if os.path.isfile(path) != expected_boolean:
            assert os.path.isfile(path) != expected_boolean
    assert os.path.isfile(path) == expected_boolean