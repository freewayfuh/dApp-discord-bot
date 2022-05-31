import json
import discord
import requests
import asyncio
from threading import Timer

from discord.utils import get
from discord.ext import commands
from core.cog_core import Cog_Extension

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# detecting price alerts
async def detectPriceAlert(bot):
    for item in bot.watchlist:
        if not item['reached']:
            floorUSD = getCollectionFloor(
                item['collection_slug']) * getEthPrice()
            targetUSD = int(item['price'])
            if item['operator'] == '>=':
                condition = (floorUSD >= targetUSD)
            elif item['operator'] == '>':
                condition = (floorUSD > targetUSD)
            elif item['operator'] == '=':
                condition = (floorUSD == targetUSD)
            elif item['operator'] == '<=':
                condition = (floorUSD <= targetUSD)
            else:
                condition = (floorUSD < targetUSD)

            if condition:
                item['reached'] = True
                title = (f'Price Reached: {item["collection_slug"]}')
                url = (
                    f'https://opensea.io/collection/{item["collection_slug"]}')
                msg = (
                    f'The floor price of {item["collection_slug"]} has just reached the target price ({item["operator"]} {item["price"]} USD).\n'
                )
                msg += (
                    f'The current floor price is {getCollectionFloor(item["collection_slug"])} ETH / {format(floorUSD, ".2f")} USD.\n'
                )
                embed = discord.Embed(title=title,
                                      url=url,
                                      description=msg,
                                      color=discord.Color.blue())
                await sendMessage(bot, embed)

    # set a thread that runs detectPriceAlert every 60 second
    await asyncio.sleep(60)
    t = Timer(60.0, await detectPriceAlert(bot))
    t.start()


# send discord notificaiton to a channel
async def sendMessage(bot, embed):
    await discord.utils.get(bot.get_all_channels(),
                            name='watchlist-alert').send(embed=embed)


def getCollectionFloor(collection_slug):
    url = f'https://api.opensea.io/api/v1/collection/{collection_slug}'
    response = requests.get(url, headers={"Accept": "application/json"})
    data = response.json()
    return data["collection"]["stats"]["floor_price"]

def getEthPrice():
    URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    r = requests.get(url=URL)
    data = r.json()
    return data[1]['current_price']

def invalidCollectionSlug(collection_slug):
    url = f'https://api.opensea.io/api/v1/collection/{collection_slug}'
    response = requests.get(url, headers={"Accept": "application/json"})
    data = response.json()
    if 'collection' in data:
        return False
    return True

def invalidOperator(operator):
    if operator in ['>=', '>', '=', '<=', '<']:
        return False
    return True

def getWatchlistMsg(bot):
    msg = ''
    counter = 1
    for item in bot.watchlist:
        reach_msg = '' if not item[
            'reached'] else '  :white_check_mark: Reached!'
        msg += (
            f'#{counter} {item["collection_slug"]}  {item["operator"]}  {item["price"]} USD{reach_msg}\n'
        )
        counter += 1
    return msg

def getCollectionFloor(collection_slug):
    url = f'https://api.opensea.io/api/v1/collection/{collection_slug}'
    response = requests.get(url, headers={"Accept": "application/json"})
    data = response.json()
    return data["collection"]["stats"]["floor_price"]


class Watchlist(Cog_Extension):
    """
    NFT price alerts for opensea
    """

    @commands.command()
    async def wl(self, ctx):
        """
        Show NFT watchlist
        """
        if self.bot.watchlist:
            msg = getWatchlistMsg(self.bot)
            embed = discord.Embed(description=msg, color=discord.Color.blue())
        else:
            msg = "You haven't added any collection to watchlist.\n"
            msg += "Please use `\wl_add <colletion_slug> <operator> <price> USD` to set the watchlist."
            embed = discord.Embed(description=msg, color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    async def wl_add(self, ctx, collection_slug: str, operator: str, price: str):
        """
        Set price alerts for NFT collections
        """
        if invalidCollectionSlug(collection_slug):
            msg = 'Please check the collection slug.'
            embed = discord.Embed(description=msg, color=discord.Color.red())
        elif invalidOperator(operator):
            msg = 'Please check the operator. Only accept `<`, `<=`, `=`, `>=`, `>`.'
            embed = discord.Embed(description=msg, color=discord.Color.red())
        elif not price.isnumeric():
            msg = 'Please check the input format: <price> must be an integer.'
            embed = discord.Embed(description=msg, color=discord.Color.red())
        else:
            obj = {
                'collection_slug': collection_slug,
                'operator': operator,
                'price': price,
                'reached': False
            }
            self.bot.watchlist.append(obj)
            msg = (
                f'Successfully set price alert for {collection_slug} at {price} USD.\n'
            )
            embed = discord.Embed(description=msg, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def wl_rm(self, ctx, number: str):
        """
        Reomove price alert for NFT collection
        """
        index = int(number) - 1
        if len(self.bot.watchlist) == 0 or 0 > index >= len(self.bot.watchlist):
            msg = 'Please check the number you want to remove.'
            embed = discord.Embed(description=msg, color=discord.Color.red())
        else:
            self.bot.watchlist.pop(index)
            msg = (f'Removed successfully.\n')
            if len(self.bot.watchlist) > 0:
                msg += (f'Watchlist now:\n{getWatchlistMsg(self.bot)}')
            embed = discord.Embed(description=msg, color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def wl_start(self, ctx):
        """
        Start detecting price for NFT collections
        """
        if self.bot.watchlist:
            msg = (f'Started detecting price alert for:\n{getWatchlistMsg(self.bot)}')
            msg += (f'Price notifications will be sent to #watchlist-alert.')
            embed = discord.Embed(description=msg, color=discord.Color.blue())
            await ctx.send(embed=embed)

            guild = ctx.guild
            category = get(guild.categories, id=jdata['subscribed_category_ID'])
            channel = get(guild.text_channels, name='watchlist-alert')
            if channel is None:
                channel = await guild.create_text_channel('watchlist-alert', category=category)
            await detectPriceAlert(self.bot)
        else:
            msg = "You haven't added any collection to watchlist.\n"
            embed = discord.Embed(description=msg, color=discord.Color.red())
            await ctx.send(embed=embed)


    @commands.command()
    async def wl_clear(self, ctx):
        """
        Clear NFT watchlist
        """
        self.bot.watchlist = []
        msg = 'Watchlist cleared successfully.'
        embed = discord.Embed(description=msg, color=discord.Color.blue())
        await ctx.send(embed=embed)


def setup(bot):
    bot.watchlist = []
    bot.add_cog(Watchlist(bot))
