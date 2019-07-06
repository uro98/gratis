import config
import discord
from discord.ext import commands
import asyncio
import logging
from reddit_scraper import RedditScraper
from game_deal_manager import GameDealManager

logging.basicConfig(level=logging.INFO)

#TODO: get channel id, fix sleep time, refactor, search function, input validation

class GratisClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.get_deals())

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.content == 'g.info':
            description = 'Gratis is a Reddit scraping bot that helps you add more games you\'ll never play to your games library!'
            embed = discord.Embed(title='Bot Information', description=description, colour=0x2df228) \
                           .add_field(name='Developer', value='[Yu-Jo Tseng](https://yujotseng.com)') \
                           .add_field(name='Source code', value='[GitHub repo](https://github.com/uro98/gratis)')
            await message.channel.send(embed=embed)
        elif message.content == 'g.help':
            embed = discord.Embed(title='Gratis Commands', colour=0x2df228) \
                           .add_field(name='g.info', value='Display bot information.', inline=False) \
                           .add_field(name='g.help', value='Display the commands menu.')
            await message.channel.send(embed=embed)

    async def get_deals(self):
        await self.wait_until_ready()

        reddit = RedditScraper()
        manager = GameDealManager(reddit)
        channel = self.get_channel(config.DISCORD_CHANNEL_ID)

        while not self.is_closed:
            if await is_8am_or_8pm():
                new_free_deals = manager.find_deals()
                if new_free_deals:
                    embed = discord.Embed(title='Freebie Alert!', description='New deals with free stuff on [/r/GameDeals](https://www.reddit.com/r/GameDeals/)', color=0x2df228)
                    for deal in new_free_deals:
                        embed.add_field(name=deal.title, value=deal.url, inline=False)
                    await client.send_message(channel, embed=embed)

            await channel.send('Going to sleep.')
            await asyncio.sleep(30)

            # sleep_until_next_posting_time()

def main():
    client = GratisClient()
    client.run(config.DISCORD_TOKEN)


# async def is_8am_or_8pm():
#     """Return true if current time is within the first minute of 8am or 8pm."""
#     return (((time.localtime().tm_hour == 8) or (time.localtime().tm_hour == 20))
#         and (time.localtime().tm_min == 0))


# def sleep_until_next_posting_time():
#     """Calculate the time until the next posting time and sleep for that duration."""
#     current_time = time.localtime()
#     print_current_time(current_time)
#     time_to_sleep = calculate_time_to_sleep(current_time)
#     print_time_to_sleep(time_to_sleep)
#     sleep(time_to_sleep)


# def print_current_time(current_time):
#     """Print the current time."""
#     print("Current time: " + str(current_time.tm_hour)
#           + ":" + str(current_time.tm_min)
#           + ":" + str(current_time.tm_sec))


# def calculate_time_to_sleep(current_time):
#     """Return the amount of time to sleep for as a tuple."""
#     extra_seconds_to_sleep = 60 - current_time.tm_sec
#     extra_minutes_to_sleep = 17 - current_time.tm_min - 1
#     hours_to_sleep = calculate_hours(current_time)
#     Time = namedtuple('Time', ['hour', 'min', 'sec'])
#     return Time(hours_to_sleep, extra_minutes_to_sleep, extra_seconds_to_sleep)


# def calculate_hours(current_time):
#     """Return the number of full hours until the next posting time."""
#     if current_time.tm_hour < 8:
#         return 8 - current_time.tm_hour - 1
#     elif current_time.tm_hour >= 8 and current_time.tm_hour < 20:
#         return 20 - current_time.tm_hour - 1
#     else:
#         return (24 - current_time.tm_hour) + 7


# def print_time_to_sleep(time_to_sleep):
#     """Print the amount of time to sleep for."""
#     print("Sleeping for "
#           + str(time_to_sleep.hour) + " hours, "
#           + str(time_to_sleep.min) + " minutes and "
#           + str(time_to_sleep.sec) + " seconds.")


# async def sleep(time_to_sleep):
#     """Sleep for the given amount of time."""
#     await asyncio.sleep(time_to_sleep.hour * 60 * 60
#                         + time_to_sleep.min * 60
#                         + time_to_sleep.sec)


if __name__ == '__main__':
    main()
