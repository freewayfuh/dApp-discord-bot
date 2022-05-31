import json
import asyncio
import discord
import numpy as np

from discord.ext import commands
from core.cog_core import Cog_Extension

from utils.utils import plot_radar_save_img, plot_hbar_save_img, predict, fetch_128_eth, fetch_collection_data_by_ranking, colorize_rise_fall, evaluate_score, mycolor

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

with open('problems.json', 'r', encoding='utf8') as jfile:
    pdata = json.load(jfile)['problems']



class Mirror(Cog_Extension):
    """
    A customised investment manager that combines psychometric evaluation with quantitative analysis of ETH/NFT
    """
    
    @commands.command()
    async def mirror(self, ctx):
        """
        Psychological test
        """
        scores = {"CN": 0, "EN": 0, "SN": 0}

        for k, d in enumerate(pdata):
            embed = discord.Embed(title="Ξ × NFT × Mind-Set", color=mycolor())
            embed.set_image(url=d["img"])
            embed.add_field(name=d["des"], value=d["ins"])
            embed.set_footer(text=f"Choose a reaction {ctx.author} can relate to the image the most.")

            if k == 0:
                msg = await ctx.send(embed=embed)
            else:
                await msg.clear_reactions()
                await msg.edit(embed=embed)

            for emo in d["btn"]:
                await msg.add_reaction(emo)

            def elig_check(reaction, user):
                if reaction.message.id != msg.id or user != ctx.message.author or str(reaction.emoji) not in d["btn"]:
                    return False
                else:
                    return True
            
            try:
                res, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=elig_check)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()
            
            if user != ctx.message.author:
                pass
            elif str(res.emoji) in d["btn"]:
                if d["inv"]:
                    scores[d["cls"]] += 6 - (int(np.argwhere(np.array(d["btn"]) == str(res.emoji))) + 1)
                else:
                    scores[d["cls"]] += int(np.argwhere(np.array(d["btn"]) == str(res.emoji))) + 1
                continue
        
        total_s_ratio = (scores["CN"]/3 + scores["EN"]/4 + scores["SN"]/2) / 15
        fn_path = "images/{}_{}_{}_plot.png".format(scores["CN"], scores["EN"], scores["SN"])
        plot_radar_save_img(fn_path, scores)
        d_f = discord.File(fn_path, filename="image.png")

        embed = discord.Embed(
            title=f"{ctx.author}'s Psychological State", color=mycolor())
        embed.add_field(name="Environmental Uncertainty", value=evaluate_score(
            total_s_ratio * 5, r=False), inline=True)
        embed.add_field(name="Environmental Threat", value=evaluate_score(
            total_s_ratio * 5, r=True), inline=True)
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text="Press ➡️ to see your Psych Eth Advice")

        await msg.delete()
        msg = await ctx.send(file=d_f, embed=embed)
        await msg.add_reaction("➡️")

        def elig_check(reaction, user):
            if reaction.message.id != msg.id or user != ctx.message.author or str(reaction.emoji) not in ["➡️"]:
                return False
            else:
                return True

        try:
            res, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=elig_check)
        except asyncio.TimeoutError:
            return await msg.clear_reactions()

        if user != ctx.message.author:
            pass
        elif str(res.emoji) in ["➡️"]:
            fn_path_eth = "images/eth_plot.png"
            pri, cap, vol = fetch_128_eth(fn_path_eth)
            prob = predict(pri, cap, vol)
            d_f1 = discord.File(fn_path_eth, filename="eth.png")

            fn_path_prob = "images/prob_plot.png"
            plot_hbar_save_img(fn_path_prob, prob, total_s_ratio)
            d_f2 = discord.File(fn_path_prob, filename="prob.png")

        embed1 = discord.Embed(title="Referred Ξ Data", color=mycolor())
        embed1.set_image(url="attachment://eth.png")

        embed2 = discord.Embed(
            title=f"Psych Ξ Advice for {ctx.author}", color=mycolor())
        embed2.set_image(url="attachment://prob.png")
        embed2.set_footer(text="Press ➡️ to see your Psych NFT Advice")

        await msg.delete()
        msg1 = await ctx.send(file=d_f1, embed=embed1)
        msg2 = await ctx.send(file=d_f2, embed=embed2)
        await msg2.add_reaction("➡️")

        def elig_check(reaction, user):
            if reaction.message.id != msg2.id or user != ctx.message.author or str(reaction.emoji) not in ["➡️"]:
                return False
            else:
                return True

        try:
            res, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=elig_check)
        except asyncio.TimeoutError:
            return await msg2.clear_reactions()

        if user != ctx.message.author:
            pass
        elif str(res.emoji) in ["➡️"]:
            try:
                df = fetch_collection_data_by_ranking()
            except:
                df = fetch_collection_data_by_ranking()

            df["abs"] = np.abs(df["nft_1_change"].astype(float)) + \
                np.abs(df["nft_7_change"].astype(float)) + \
                np.abs(df["nft_30_change"].astype(float))
            df.sort_values(by=['abs'], inplace=True)
            df["rank"] = df["abs"].rank(pct=True)

            ratio = 1 - total_s_ratio  # larger total_s_ratio => more conser. => less change
            idx = int(
                df.iloc[(df['rank']-ratio).abs().argsort()[:1]].index.tolist()[0])

        embed = discord.Embed(
            title=f"Psych NFT Advice for {ctx.author}", color=mycolor())
        embed.set_thumbnail(
            url=df["nft_img"][idx])

        current_name = df["nft_name"][idx]
        current_slug = df["nft_slug"][idx]
        embed.add_field(
            name="NFT", value=f"[{current_name}](https://opensea.io/collection/{current_slug})", inline=True)

        current_price = np.round(float(df["floor_price"][idx]), 2)
        embed.add_field(name="Floor Price",
                        value=f"{current_price} Ξ", inline=True)

        embed.add_field(
            name="24-hour", value=colorize_rise_fall(df["nft_1_change"][idx]), inline=True)
        embed.add_field(
            name="7-days", value=colorize_rise_fall(df["nft_7_change"][idx]), inline=True)
        embed.add_field(
            name="30-days", value=colorize_rise_fall(df["nft_30_change"][idx]), inline=True)

        await msg1.delete()
        await msg2.delete()
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rank(self, ctx, num_nfts=20, sortby=1):
        """
        Show out Top collection
        """
        try:
            df = fetch_collection_data_by_ranking(
                num_nfts=num_nfts+1, sortby=sortby)
        except:
            df = fetch_collection_data_by_ranking(
                num_nfts=num_nfts+1, sortby=sortby)

        num_days = sortby if sortby != 0 else "All"

        embed = discord.Embed(
            title=f"NFT Ranking Sorted by {num_days}-Day Volume", color=mycolor())
        embed.set_thumbnail(
            url="https://seeklogo.com/images/O/open-sea-logo-0FFCF87312-seeklogo.com.png")

        for i in range(num_nfts):
            embed.add_field(name="Rank", value=f"{i+1}", inline=True)

            current_name = df["nft_name"][i]
            current_slug = df["nft_slug"][i]
            embed.add_field(
                name="NFT", value=f"[{current_name}](https://opensea.io/collection/{current_slug})", inline=True)

            current_price = np.round(float(df["floor_price"][i]), 2)
            embed.add_field(name="Floor Price",
                            value=f"{current_price} Ξ", inline=True)

            embed.add_field(
                name="24-hour", value=colorize_rise_fall(df["nft_1_change"][i]), inline=True)
            embed.add_field(
                name="7-days", value=colorize_rise_fall(df["nft_7_change"][i]), inline=True)
            embed.add_field(
                name="30-days", value=colorize_rise_fall(df["nft_30_change"][i]), inline=True)

            if (i+1) % 4 == 0 or i == num_nfts-1:
                await ctx.send(embed=embed)

                embed = discord.Embed(
                    title=f"NFT Ranking Sorted by {num_days}-Day Volume", color=mycolor())
                embed.set_thumbnail(
                    url="https://seeklogo.com/images/O/open-sea-logo-0FFCF87312-seeklogo.com.png")


def setup(bot):
    bot.add_cog(Mirror(bot))