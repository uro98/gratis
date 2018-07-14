import config
import praw
import time
import re
from collections import deque


def main():
    game_deals_sub = get_subreddit('GameDeals')
    search_limit = 30
    seen_deal_ids = deque(maxlen=search_limit)

    while True:
        if is_8am_or_8pm():
            new_free_deals = find_deals(game_deals_sub, seen_deal_ids, search_limit)
            if new_free_deals:
                print("Posting on Discord.")  # (message, (title, link)*)
        sleep_until_next_posting_time()


def get_subreddit(name):
    """Return the subreddit instance."""
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         password=config.PASSWORD,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME)
    reddit.read_only = True
    return reddit.subreddit(name)


def is_8am_or_8pm():
    """Return true if current time is within the first minute of 8am or 8pm."""
    return (((time.localtime().tm_hour == 8) or (time.localtime().tm_hour == 20))
        and (time.localtime().tm_min == 0))


def find_deals(game_deals_sub, seen_deal_ids, search_limit):
    """Return new free deals on the subreddit."""
    new_free_deals = []
    for deal in game_deals_sub.new(limit=search_limit):
        process_deal(deal, seen_deal_ids, new_free_deals)
    return new_free_deals


def process_deal(deal, seen_deal_ids, new_free_deals):
    """Store the deal if it has not been seen before and is free."""
    if deal.id not in seen_deal_ids and is_free_deal(deal):
        new_free_deals.append(deal)
        print("Added: " + deal.title)
    seen_deal_ids.append(deal.id)


def is_free_deal(deal):
    """Return True if the deal title contains free as a word or 100%."""
    # Match 'free' as a complete word (case insensitive)
    match_free = re.search(r'\bfree\b', deal.title, re.IGNORECASE)
    # Match '100%' or '100 %'
    match_100 = re.search('100 *%', deal.title)
    if match_free or match_100:
        return True


def sleep_until_next_posting_time():
    """Calculate the time until the next posting time and sleep for that duration."""
    current_time = time.localtime()
    extra_minutes_to_sleep = 60 - current_time.tm_min
    hours_to_sleep = calculate_hours_to_sleep(current_time)
    print("Sleeping for "
          + str(hours_to_sleep) + " hours and "
          + str(extra_minutes_to_sleep) + " minutes.")
    time.sleep(hours_to_sleep * 60 * 60 + extra_minutes_to_sleep * 60)


def calculate_hours_to_sleep(current_time):
    """Return the number of full hours until the next posting time."""
    if current_time.tm_hour < 8:
        return 8 - current_time.tm_hour - 1
    elif current_time.tm_hour >= 8 and current_time.tm_hour < 20:
        return 20 - current_time.tm_hour - 1
    else:
        return (24 - current_time.tm_hour) + 7


if __name__ == '__main__':
    main()
