import os
import json
import discord
import requests

from discord.ext import commands
from core.cog_core import Cog_Extension
from datetime import datetime, timezone, timedelta


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

def add_info(name, address):
    info = {}
    info[name] = address
    with open("./info_book.json", "r+") as file:
        if os.stat("./info_book.json").st_size == 0:
            # print("file is empty!")
            json.dump(info, file)
        else: 
            # print("file is not empty!")
            data = json.loads(file.read())
            data.update(info)
            file.seek(0)
            json.dump(data, file)

def get_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={jdata['etherscan_API_key']}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data['result']

def get_gasinfo():
    url = f"https://owlracle.info/eth/gas?apikey={jdata['owlracle_API_key']}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def getEthPrice():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    response = requests.get(url)
    data = json.loads(response.text)
    return data[1]['current_price']


class ETH(Cog_Extension):
    """
    ETH data query
    """

    @commands.command()
    async def eth(self, ctx):
        """
        Show current ETH price (USD)
        """
        msg = str(getEthPrice()) + ' USD'
        embed = discord.Embed(description=msg, color=discord.Color.blue())
        await ctx.send(embed=embed)
    
    @commands.command()
    async def add(self, ctx, address: str):
        """
        Add wallet address
        """
        author = str(ctx.author)
        add_info(author, address)
        embed = discord.Embed(title=f"\U0001F44B **Hello {author}!**", description=f"You have successfully added your address information: **{address}**. \u2713", color=0xFFA46E)
        await ctx.send(embed=embed)

    @commands.command()
    async def balance(self, ctx):
        """
        Show your balance on the ETH Blockchain
        """
        with open("./info_book.json", "r") as file:
            data = json.loads(file.read())
        
        if str(ctx.author) in data:
            address = data[str(ctx.author)]
            balance = get_balance(address)
            await ctx.send(balance)
        else:
            await ctx.send("沒有這個人的資料哦！")

    @commands.command()
    async def gas(self, ctx):
        """
        Show current gas prices
        """
        data = get_gasinfo()['speeds']

        slowPrice, slowUs = data[0]['gasPrice'], data[0]['estimatedFee']
        standardPrice, standardUs = data[1]['gasPrice'], data[1]['estimatedFee']
        fastPrice, fastUs = data[2]['gasPrice'], data[2]['estimatedFee']
        instantPrice, instantUs = data[3]['gasPrice'], data[3]['estimatedFee']

        embed = discord.Embed(title=u"\u26FD **Gas Prices**", color=0xffa46e, timestamp=datetime.now(tz=timezone(timedelta(hours=8))))
        embed.set_thumbnail(url="https://owlracle.info/img/owl.webp")
        embed.add_field(name="**Slow** \U0001F6F4", value=f'{slowPrice:.2f} Gwei ({slowUs:.2f} USD)', inline=False)
        embed.add_field(name="**Standard** \U0001F697", value=f'{standardPrice:.2f} Gwei ({standardUs:.2f} USD)', inline=False)
        embed.add_field(name=u"**Fast** \u2708", value=f'{fastPrice:.2f} Gwei ({fastUs:.2f} USD)', inline=False)
        embed.add_field(name="**Instant** \U0001F680", value=f'{instantPrice:.2f} Gwei ({instantUs:.2f} USD)', inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ETH(bot))