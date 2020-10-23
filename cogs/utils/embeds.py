import discord
import datetime

class MyEmbeds():
    
    @classmethod
    def create_error(cls, title, description : str = None, exception : Exception = None):
        return discord.Embed(
            title = title or "Error",
            description = description or f"{type(exception).__name__}: {exception}",
            color = 0xff0000
        )

    @classmethod
    def create_success(cls, title, description):
        return discord.Embed(
            title = title or "Error",
            description=description,
            color = 0x00ff00
        )


    @classmethod
    def create_add_money(cls, amount : int, member : discord.Member, request: discord.Member):
        return discord.Embed(
            title = "Bank Update",
            color=discord.Color.green(),
            description=f"Added {amount} **CR** to {member.mention}'s balance",
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        ).set_footer(
            text=f"requested by {str(request)}",
            icon_url=request.avatar_url
        )

    @classmethod
    def create_remove_money(cls, amount : int, member : discord.Member, request: discord.Member):
        return discord.Embed(
            title = "Bank Update",
            color=discord.Color.orange(),
            description=f"Removed {amount} **CR** from {member.mention}'s balance",
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        ).set_footer(
            text=f"requested by {str(request)}",
            icon_url=request.avatar_url
        )
    
    @classmethod
    def create_job(cls, job_info : str):
        return discord.Embed(
            title="💼  Job",
            color=discord.Color.blue(),
            description=job_info,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        ).set_footer(
            text=f"React with ✅ to accept"
        )

    @classmethod
    def create_job_accepted(cls, job_info : str, by : discord.Member, contractor : discord.Member):
        return discord.Embed(
            title="✅  Job accepted",
            color=discord.Color.green(),
            description=job_info,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        ).add_field(
            name="By:",
            value=by.mention
        ).add_field(
            name="Contractor:",
            value=contractor.mention
        )

    @classmethod
    def create_show_balance(cls, amount : int, member : discord.Member):
        return discord.Embed(
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        ).add_field(
            name="Balance:",
            value=f"{amount} **CR**"
        ).set_author(
            name=str(member),
            icon_url=member.avatar_url
        )
    

    
    

