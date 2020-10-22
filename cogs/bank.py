import discord
from discord.ext import commands

import typing

from .utils import database as db, config
from .utils.embeds import MyEmbeds as embeds

class ToMemberID(commands.Converter):
    async def convert(self, ctx, argument):
        return argument

class Bank(commands.Cog):

    """Bank commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, member: typing.Union[discord.Member], amount : int):
        """Adds money to a player"""

        old_amount = db.get_money(member.id)    
        new_amount = old_amount + amount

        db.update_money(member.id, new_amount)

        await ctx.send(f"Added {amount} to {member.mention} \nNew Balance: {new_amount}")


    @commands.command()
    async def sub(self, ctx, member: typing.Union[discord.Member], amount : int):
        """Adds money to a player"""

        old_amount = db.get_money(member.id)
        new_amount = old_amount - amount

        db.update_money(member.id, new_amount)

        await ctx.send(f"Subtracted {amount} from {member.mention} \nNew Balance: {new_amount}")


    @commands.command(aliases=["balance"])
    async def bal(self, ctx, member: typing.Optional[discord.Member]):
        """Adds money to a player"""

        if not member:
            member = ctx.author
            
        amount = db.get_money(member.id)
        await ctx.send(amount)

def setup(bot):
    bot.add_cog(Bank(bot))
    