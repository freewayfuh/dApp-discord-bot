import json
import discord
import requests

from discord.utils import get
from discord.ext import tasks
from core.cog_core import Cog_Extension
from datetime import datetime, timezone, timedelta


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Background_task(Cog_Extension):
    """
    Background task
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update.start()
    
    @tasks.loop(hours=24)
    async def update(self):
        guild = self.bot.get_guild(jdata['guild_ID'])
        category = get(guild.categories, id=jdata['subscribed_category_ID'])

        for channel in category.channels:
            if channel.id == jdata['watchlist_channel_ID']:
                continue
            print(f"Name: {channel} Id: {channel.id}")

            url = "https://api.opensea.io/api/v1/collection/" + str(channel)
            response = requests.get(url, headers={"Accept": "application/json"})
            data = json.loads(response.text)

            stats = data['collection']['stats']
            name = data['collection']['name']
            icon = data['collection']['image_url']
            external_url = data['collection']['external_url']
            
            one_day_volume = stats['one_day_volume']
            one_day_change = stats['one_day_change']
            one_day_sales = stats['one_day_sales']
            one_day_average_price = stats['one_day_average_price']

            if(one_day_volume != 0):
                embed = discord.Embed(title=name, url=external_url, color=0xffa46e, timestamp=datetime.now(tz=timezone(timedelta(hours=8))))
                embed.set_thumbnail(url=icon)

                embed.add_field(name='Today\'s volume', value=f'{one_day_volume:.2f} ETH', inline=False)
                embed.add_field(name='Today\'s change', value=f'{one_day_change:.2f} ETH', inline=False)
                embed.add_field(name='Today\'s sales', value=f'{one_day_sales:.2f} NFT', inline=False)

                embed.add_field(name='Today\'s average price', value=f'{one_day_average_price:.2f} ETH', inline=False)
                await channel.send(embed=embed)
            else:
                embed=discord.Embed(title='[ERROR] cannot fetch data because the collection is too new', color=0xffa46e)
                await channel.send(embed=embed)
    
    @update.before_loop
    async def before_update(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Background_task(bot))