import discord
from discord.ext import commands

import typing

from .utils import database as db, config, checks
from .utils.embeds import MyEmbeds as embeds

def has_moderator_role():
    def predicate(ctx):
        moderator_role = db.get_settings(ctx.guild.id, "moderator_role")

        if not moderator_role:
            raise checks.NoSetup

        roles_ids = [x.id for x in ctx.author.roles]
        return moderator_role in roles_ids
    return commands.check(predicate)

class Bank(commands.Cog):

    """Bank commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        if payload.member.bot:
            return

        channel = self.bot.get_channel(payload.channel_id)
        guild = self.bot.get_guild(payload.guild_id)

        job_channel_id = db.get_settings(payload.guild.id, "job_channel")

        if not job_channel_id:
            return
        
        job_channel = self.bot.get_channel(job_channel_id)

        if str(payload.emoji) == "✅" and db.get_job_info(payload.message_id, "message"):

            description = db.get_job_info(payload.message_id, "description")

            auftraggeber_id = db.get_job_info(payload.message_id, "member")
            auftraggeber = guild.get_member(auftraggeber_id)


            await job_channel.send(embed=embeds.create_job_accepted(description, auftraggeber, payload.member))

            msg = await channel.fetch_message(payload.message_id)
            await msg.delete()
            
            db.remove_job(payload.message_id)

    @commands.command()
    @has_moderator_role()
    async def add(self, ctx, member: typing.Union[discord.Member], amount : int):
        """Adds money to a member"""

        old_amount = db.get_money(member.id)    
        new_amount = old_amount + amount

        db.update_money(member.id, new_amount)

        await ctx.send(embed=embeds.create_add_money(amount, member, ctx.author))


    @commands.command(aliases=["remove"])
    @has_moderator_role()
    async def sub(self, ctx, member: typing.Union[discord.Member], amount : int):
        """Subtracts money to a member"""

        old_amount = db.get_money(member.id)
        new_amount = old_amount - amount

        db.update_money(member.id, new_amount)

        await ctx.send(embed=embeds.create_remove_money(amount, member, ctx.author))


    @commands.command(aliases=["balance"])
    async def bal(self, ctx, member: typing.Optional[discord.Member]):
        """Shows Balance of a member"""

        if not member:
            member = ctx.author

        amount = db.get_money(member.id)
        await ctx.send(embed=embeds.create_show_balance(amount, member))

    @commands.command()
    @has_moderator_role()
    async def job(self, ctx, *, description: str):
        """Creates a job offer"""
        
        job_message = await ctx.send(embed=embeds.create_job(description))

        await job_message.add_reaction("✅")
        db.add_job(ctx.guild.id, job_message.id, ctx.author.id, description)

        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Bank(bot))
    