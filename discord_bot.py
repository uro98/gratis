import config
import discord
import asyncio
import logging
import traceback
from datetime import datetime
from reddit_scraper import RedditScraper
from game_deal_manager import GameDealManager

logging.basicConfig(level=logging.INFO)

# TODO: persistent data, log to file

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

    async def on_error(event, *args, **kwargs):
        message = args[0]
        logging.warning(traceback.format_exc())

    async def get_deals(self):
        await self.wait_until_ready()

        reddit = RedditScraper()
        manager = GameDealManager(reddit)
        channel = self.get_channel(config.DISCORD_CHANNEL_ID)

        while not self.is_closed():
            if self.__is_6am_or_6pm():
                new_free_deals = manager.find_deals()

                if new_free_deals:
                    embed = discord.Embed(
                            title='Freebie Alert!',
                            description='New deals with free stuff on [/r/GameDeals](https://www.reddit.com/r/GameDeals/)',
                            color=0x2df228)
                    for deal in new_free_deals:
                        embed.add_field(name=deal.title, value=deal.url, inline=False)
                    await self.__send_deals(embed)
                    
                await asyncio.sleep(10 * 60 * 60 + 55 * 60) # Sleep for 10 hours and 55 minutes
            else:
                await asyncio.sleep(1)

    def __is_6am_or_6pm(self):
        """Return true if current time is within the first minute of 6am or 6pm."""
        current_time = datetime.now()
        return ((current_time.hour == 6) or (current_time.hour == 21)) and (current_time.minute == 20)

    async def __send_deals(self, embed):
        channels_to_send_to = [c for c in self.get_all_channels() if c.type == discord.ChannelType.text and c.name == 'free-games']

        for channel in channels_to_send_to:
            if channel.permissions_for(channel.guild.me).send_messages:
                await channel.send(embed=embed)
            else:
                await channel.send('I don\'t have the permission to send messages in this channel!')


def main():
    client = GratisClient()
    client.run(config.DISCORD_TOKEN)

if __name__ == '__main__':
    main()
