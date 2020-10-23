import discord
from discord.ext import commands

from .utils import database, config
from .utils.embeds import MyEmbeds as embeds

class Admin(commands.Cog):

    """Debugging and Admin-Only Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module : str):
        """Loads a module"""

        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(embed=embeds.create_error("Failed loading Extension", e))
        else:
            await ctx.send(embed=embeds.create_success("Success", "Successfully loaded extension"))


    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module : str):
        """Unloads a module"""

        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(embed=embeds.create_error("Failed unloading Extension", e))
        else:
            await ctx.send(embed=embeds.create_success("Success", "Successfully unloaded extension"))


    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module"""

        try:
            self.bot.reload_extension(module)
        except Exception as e:
            await ctx.send(embed=embeds.create_error("Failed reload Extension", e))
        else:    
            await ctx.send(embed=embeds.create_success("Success", "Successfully reloaded extension"))



def setup(bot):
    bot.add_cog(Admin(bot))
    