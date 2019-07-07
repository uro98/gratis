import re
from collections import deque
from reddit_scraper import RedditScraper


class GameDealManager:

    num_of_deals = 30
    
    def __init__(self, reddit):
        self.__reddit = reddit
        self.__seen_deal_ids = deque(maxlen=GameDealManager.num_of_deals)

    def find_deals(self):
        """Return new free deals on the subreddit."""
        new_free_deals = []
        for deal in self.__reddit.get_new_posts_in_sub(GameDealManager.num_of_deals, 'GameDeals'):
            self.__process_deal(deal, new_free_deals)
        return new_free_deals

    def __process_deal(self, deal, new_free_deals):
        """Store the deal if it has not been seen before and is free."""
        if deal.id not in self.__seen_deal_ids and self.__is_free_deal(deal):
        #if is_free_deal(deal):
            new_free_deals.append(deal)
        self.__seen_deal_ids.append(deal.id)

    def __is_free_deal(self, deal):
        """Return True if the deal title contains free as a word or 100%."""
        # Match 'free' as a complete word (case insensitive)
        match_free = re.search(r'\bfree\b', deal.title, re.IGNORECASE)
        # Match '100%' or '100 %'
        match_100 = re.search('100 *%', deal.title)
        return match_free or match_100


if __name__ == '__main__':
    reddit = RedditScraper()
    manager = GameDealManager(reddit)
    deals = manager.find_deals()
    for deal in deals:
        print(deal.title)
