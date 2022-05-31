import json
import discord
import requests

from discord.utils import get
from discord.ext import commands
from core.cog_core import Cog_Extension
from datetime import datetime, timezone, timedelta

import random


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

with open("collection_list.json") as file:
    collection_list = json.load(file)

class Opensea(Cog_Extension):
    """
    Opensea data query
    """

    @commands.command()
    async def draw(self, ctx):
        """
        Random show a collection
        """
        collection_name = random.choice(collection_list)
        url = f"https://api.opensea.io/api/v1/collection/{collection_name}"
        response = requests.get(url, headers={"Accept": "application/json"})
        data = json.loads(response.text)

        stats = data['collection']['stats']
        name = data['collection']['name']
        icon = data['collection']['image_url']
        external_url = data['collection']['external_url']
        
        total_volume = stats['total_volume']
        total_sales = stats['total_sales']
        total_supply = stats['total_supply']
        num_owners = stats['num_owners']
        average_price = stats['average_price']
        num_reports = stats['num_reports']
        market_cap = stats['market_cap']
        floor_price = 0.0 if stats['floor_price'] == None else stats['floor_price']

        if(total_volume != 0):
            embed=discord.Embed(title=name, url=external_url, color=0x009dff, timestamp=datetime.now(tz=timezone(timedelta(hours=8))))
            embed.set_thumbnail(url=icon)

            embed.add_field(name='# of owners', value=f'{num_owners:.2f}', inline=True)
            embed.add_field(name='# of reports', value=f'{num_reports:.2f}', inline=True)
            embed.add_field(name='market cap', value=f'{market_cap:.2f} ETH', inline=True)

            embed.add_field(name='total volume', value=f'{total_volume:.2f} ETH', inline=True)
            embed.add_field(name='total sales', value=f'{total_sales:.2f} NFT', inline=True)
            embed.add_field(name='total supply', value=f'{total_supply:.2f} NFT', inline=True)

            embed.add_field(name='floor price', value=f'{floor_price:.2f} ETH', inline=True)
            embed.add_field(name='average price', value=f'{average_price:.2f} ETH', inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title='[ERROR] cannot fetch data because the collection is too new', color=0x009dff)
            await ctx.send(embed=embed)


    @commands.command()
    async def nft(self, ctx, collection_name: str):
        """
        Show the collection realtime data
        """
        url = f"https://api.opensea.io/api/v1/collection/{collection_name}"
        response = requests.get(url, headers={"Accept": "application/json"})
        data = json.loads(response.text)

        stats = data['collection']['stats']
        name = data['collection']['name']
        icon = data['collection']['image_url']
        external_url = data['collection']['external_url']
        
        total_volume = stats['total_volume']
        total_sales = stats['total_sales']
        total_supply = stats['total_supply']
        num_owners = stats['num_owners']
        average_price = stats['average_price']
        num_reports = stats['num_reports']
        market_cap = stats['market_cap']
        floor_price =  0.0 if stats['floor_price'] == None else stats['floor_price']

        if(total_volume != 0):
            embed=discord.Embed(title=name, url=external_url, color=0x009dff, timestamp=datetime.now(tz=timezone(timedelta(hours=8))))
            embed.set_thumbnail(url=icon)

            embed.add_field(name='# of owners', value=f'{num_owners:.2f}', inline=True)
            embed.add_field(name='# of reports', value=f'{num_reports:.2f}', inline=True)
            embed.add_field(name='market cap', value=f'{market_cap:.2f} ETH', inline=True)

            embed.add_field(name='total volume', value=f'{total_volume:.2f} ETH', inline=True)
            embed.add_field(name='total sales', value=f'{total_sales:.2f} NFT', inline=True)
            embed.add_field(name='total supply', value=f'{total_supply:.2f} NFT', inline=True)

            embed.add_field(name='floor price', value=f'{floor_price:.2f} ETH', inline=True)
            embed.add_field(name='average price', value=f'{average_price:.2f} ETH', inline=True)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title='[ERROR] cannot fetch data because the collection is too new', color=0x009dff)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def nft_history(self, ctx, collection_name: str):
        """
        Show the collection history data
        """
        url = f"https://api.opensea.io/api/v1/collection/{collection_name}"
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
        seven_day_volume = stats['seven_day_volume']
        seven_day_change = stats['seven_day_change']
        seven_day_sales = stats['seven_day_sales']
        seven_day_average_price = stats['seven_day_average_price']
        thirty_day_volume = stats['thirty_day_volume']
        thirty_day_change = stats['thirty_day_change']
        thirty_day_sales = stats['thirty_day_sales']
        thirty_day_average_price = stats['thirty_day_average_price']

        if(one_day_volume != 0):
            embed=discord.Embed(title=name, url=external_url, color=0xffa46e, timestamp=datetime.now(tz=timezone(timedelta(hours=8))))
            embed.set_thumbnail(url=icon)

            embed.add_field(name='1 day volume', value=f'{one_day_volume:.2f} ETH', inline=True)
            embed.add_field(name='1 day change', value=f'{one_day_change:.2f} ETH', inline=True)
            embed.add_field(name='1 day sales', value=f'{one_day_sales:.2f} NFT', inline=True)

            embed.add_field(name='1 day average price', value=f'{one_day_average_price:.2f} ETH', inline=False)

            embed.add_field(name='7 day volume', value=f'{seven_day_volume:.2f} ETH', inline=True)
            embed.add_field(name='7 day change', value=f'{seven_day_change:.2f} ETH', inline=True)
            embed.add_field(name='7 day sales', value=f'{seven_day_sales:.2f} NFT', inline=True)

            embed.add_field(name='7 day average price', value=f'{seven_day_average_price:.2f} ETH', inline=False)

            embed.add_field(name='30 day volume', value=f'{thirty_day_volume:.2f} ETH', inline=True)
            embed.add_field(name='30 day change', value=f'{thirty_day_change:.2f} ETH', inline=True)
            embed.add_field(name='30 day sales', value=f'{thirty_day_sales:.2f} NFT', inline=True)

            embed.add_field(name='30 day average price', value=f'{thirty_day_average_price:.2f} ETH', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title='[ERROR] cannot fetch data because the collection is too new', color=0xffa46e)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def subscribe(self, ctx, collection_name: str):
        """
        Add the collection to subscribed channel
        """
        guild = ctx.guild
        category = get(guild.categories, id=jdata['subscribed_category_ID'])
        channel = await guild.create_text_channel(collection_name, category=category)

        url = f"https://api.opensea.io/api/v1/collection/{collection_name}"
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
            embed=discord.Embed(title=name, url=external_url, color=0xffa46e, timestamp=datetime.now(tz=timezone(timedelta(hours=8))))
            embed.set_thumbnail(url=icon)

            embed.add_field(name='Today\'s volume', value=f'{one_day_volume:.2f} ETH', inline=False)
            embed.add_field(name='Today\'s change', value=f'{one_day_change:.2f} ETH', inline=False)
            embed.add_field(name='Today\'s sales', value=f'{one_day_sales:.2f} NFT', inline=False)

            embed.add_field(name='Today\'s average price', value=f'{one_day_average_price:.2f} ETH', inline=False)

            await channel.send(embed=embed)
        else:
            embed=discord.Embed(title='[ERROR] cannot fetch data because the collection is too new', color=0xffa46e)
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Opensea(bot))