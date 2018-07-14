import config
import praw
import time
import re
import asyncio
from collections import deque, namedtuple


def get_subreddit(name):
    """Return the subreddit instance."""
    reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                         client_secret=config.REDDIT_CLIENT_SECRET,
                         password=config.REDDIT_PASSWORD,
                         user_agent=config.REDDIT_USER_AGENT,
                         username=config.REDDIT_USERNAME)
    reddit.read_only = True
    return reddit.subreddit(name)


def find_deals(game_deals_sub, seen_deal_ids, search_limit):
    """Return new free deals on the subreddit."""
    new_free_deals = []
    for deal in game_deals_sub.new(limit=search_limit):
        process_deal(deal, seen_deal_ids, new_free_deals)
    return new_free_deals


def process_deal(deal, seen_deal_ids, new_free_deals):
    """Store the deal if it has not been seen before and is free."""
    #if deal.id not in seen_deal_ids and is_free_deal(deal):
    if is_free_deal(deal):
        new_free_deals.append(deal)
    seen_deal_ids.append(deal.id)


def is_free_deal(deal):
    """Return True if the deal title contains free as a word or 100%."""
    # Match 'free' as a complete word (case insensitive)
    match_free = re.search(r'\bfree\b', deal.title, re.IGNORECASE)
    # Match '100%' or '100 %'
    match_100 = re.search('100 *%', deal.title)
    if match_free or match_100:
        return True
