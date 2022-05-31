import os
import json
import discord
from discord.ext import commands
from pretty_help import PrettyHelp
from core.cog_core import Cog_Extension


with open('./setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Bot(Cog_Extension):
    """
    Bot base command
    """

    @commands.command()
    async def load(self, ctx, extension):
        """
        Load extension
        """
        bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension} done.')

    @commands.command()
    async def unload(self, ctx, extension):
        """
        Unload extension
        """
        bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Un - Loaded {extension} done.')

    @commands.command()
    async def reload(self, ctx, extension):
        """
        Reload extension
        """
        bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Re - Loaded {extension} done.')

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='\\', intents=discord.Intents.all(), help_command=PrettyHelp())

    @bot.event
    async def on_ready():
        print(">> Bot is online <<")

    bot.add_cog(Bot(bot))

    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            bot.load_extension(f'cmds.{filename[:-3]}')
    
    bot.run(jdata['TOKEN'])