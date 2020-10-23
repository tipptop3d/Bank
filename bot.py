import sys
import traceback

import discord
from discord.ext import commands

import cogs
from cogs.utils import config, database, checks
from cogs.utils.embeds import MyEmbeds as embeds

description = """
Utility Bot written by TippTop. Work in Progress
"""

initial_extensions = (
    "cogs.admin",
    "cogs.bank",
    "cogs.settings"
)

default_prefix = "b!"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or(default_prefix),
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot is ready on Python version {sys.version}")

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send(embed=embeds.create_error(title='No Private Message', description='This command cannot be used in private messages'))
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send(embed=embeds.create_error(title='Command Disabled', description='Sorry. This command is disabled and cannot be used.'))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embeds.create_error(title='Missing Required Argument', description=f'Use Syntax: `b!{ctx.invoked_with}{" " + ctx.invoked_subcommand if ctx.invoked_subcommand else ""} {ctx.command.signature}`'))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.author.send(embed=embeds.create_error(title='Missing Permissions', description='Sorry. You lack permissions to run this command.'))
    elif isinstance(error, commands.MissingRole):
        await ctx.author.send(embed=embeds.create_error(title='Missing Role', description='Sorry. You lack a role to run this command.'))
    elif isinstance(error, checks.NoSetup):
        await ctx.send(embed=embeds.create_error(title='Missing Setup', description='Make sure to setup the moderator role'))
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(embed=embeds.create_error(title='Error', exception=error))

bot.run(config.BOT_TOKEN)
