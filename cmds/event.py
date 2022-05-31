from discord.ext import commands
from core.cog_core import Cog_Extension


class Event(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Event(bot))