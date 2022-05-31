import os
import sys
import json
import random
import discord
import local.opensea_tracker as ot

from discord.ext import commands
from core.cog_core import Cog_Extension


if not os.path.isfile("setting.json"):
    sys.exit("'setting.json' not found\ Please add it and try again.")
else:
    with open("setting.json") as file:
        config = json.load(file)

with open("collection_list.json") as file:
    collection_list = json.load(file)

class Dune(Cog_Extension):
    """
    Dune data query
    """

    @commands.command()
    async def ls(self, ctx):
        """
        Random list 5 collection
        """
        col_num = 5
        random.shuffle(collection_list)
        str_list = []
        str_list.append("```\n")
        str_list.append(f"Random pick {col_num} collection:\n")
        for i in range(5):
            str_list.append(f"{i+1}. {collection_list[i]}\n")
        str_list.append("```")
        await ctx.send("".join(str_list))


    # @commands.command()
    # async def rank(self, ctx):
    #     """
    #     Show out Top 10 collection
    #     """
    #     rank_num = 10
    #     rank_list = ot.check_ranking(rank_num+1)
    #     new_list = []
    #     new_list.append("```\n")
    #     new_list.append(f"Top {rank_num} NFTs Today:\n")
    #     for i in range(len(rank_list)):
    #         new_list.append(f"{i+1}. {rank_list[i]}\n")
    #     new_list.append("```")
    #     await ctx.send("".join(new_list))


    @commands.command()
    async def daily(self, ctx):
        """
        Send an OpenSea Daily USD volume image
        """
        title = 'Opensea Daily USD volume'
        path = './img/Opensea-Daily-USD-volume.png'
        file = discord.File(path, filename="Opensea-Daily-USD-volume.png")
        embed = discord.Embed(title=title + "📈💰", color=0x00ff00)
        embed.set_image(url=f"attachment://Opensea-Daily-USD-volume.png")
        await ctx.send(file=file, embed=embed)



    @commands.command()
    async def users(self, ctx):
        """
        Send an OpenSea active users image
        """
        title = 'OpenSea Active Users'
        path = './img/OpenSea-Active-Users.png'

        file = discord.File(path, filename="OpenSea-Active-Users.png")
        embed = discord.Embed(title=title + "🙍‍♂️🙍‍♀️", color=0x00ff00)
        embed.set_image(url=f"attachment://OpenSea-Active-Users.png")
        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def rt(self, ctx):
        """
        Send real-time OpenSea data
        """
        tmp_dict = ot.today_summarize()
        users = tmp_dict['users']
        volume = tmp_dict['volume']
        nfts_sold = tmp_dict['nfts_sold']
        embed=discord.Embed(
            title="OpenSea Realtime Data", 
            url="https://dune.com/pancakephd/Opensea-volume",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url="https://seeklogo.com/images/O/opensea-logo-7DE9D85D62-seeklogo.com.png")
        embed.add_field(name="Active Users", value=users, inline=False)
        embed.add_field(name="NFTs Sold", value=nfts_sold, inline=False)
        embed.add_field(name="Volume(USD)", value=volume, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Dune(bot))