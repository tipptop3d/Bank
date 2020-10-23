import discord
from discord.ext import commands

import typing

from .utils import database as db, config, checks
from .utils.embeds import MyEmbeds as embeds

class Settings(commands.Cog):

    """Commands for Setup"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-job-channel")
    @commands.has_guild_permissions(manage_guild = True)
    async def set_job_channel(self, ctx, channel: typing.Optional[discord.TextChannel]):
        """Sets jobs channel, leave blank to remove"""

        db.update_job_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Jobs Channel was set to {channel.mention}")

    @commands.command(name="set-moderator-role")
    @commands.has_guild_permissions(manage_guild = True)
    async def set_moderator_role(self, ctx, role : typing.Union[discord.Role]):

        db.update_moderator_role(ctx.guild.id, role.id)
        await ctx.send(f"Moderator Role was set to {role.mention}")



def setup(bot):
    bot.add_cog(Settings(bot))
    