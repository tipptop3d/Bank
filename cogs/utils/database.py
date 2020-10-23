import sqlite3

conn = sqlite3.connect('bank.db')

conn.row_factory = sqlite3.Row

c = conn.cursor()

def get_money(member_id : int):
    c.execute(f"SELECT * FROM money WHERE member=:member_id", {"member_id": member_id})
    
    row = c.fetchone()

    if row:
        money = row["amount"]
    else:
        money = 0

    return money

def update_money(member_id : int, amount : int):
    c.execute("SELECT * FROM money WHERE member=:member_id", {"member_id": member_id})

    with conn:
        if c.fetchone():
            c.execute("UPDATE money SET amount = :amount WHERE member = :member_id", {"member_id": member_id, "amount": amount})
        else:
            c.execute("INSERT INTO money VALUES (:member_id, :amount)", {"member_id": member_id, "amount": amount})

def delete_money_entry(member_id : int):
    with conn:
        c.execute(f"DELETE FROM money WHERE member=:member_id", {"member_id": member_id})


def get_settings(guild_id : int, column : str):
    c.execute(f"SELECT * FROM settings WHERE guild=:guild_id", {"guild_id": guild_id})
    row = c.fetchone()

    if row:
        result = row[column]
    else:
        result = None
    return result

def update_job_channel(guild_id : int, channel_id : int):
    with conn:
        if get_settings(guild_id, "guild"):
            c.execute("UPDATE settings SET job_channel = :channel_id WHERE guild = :guild_id", {"guild_id": guild_id, "channel_id": channel_id})
        else:
            c.execute("INSERT INTO settings VALUES (:guild_id, :channel_id, :moderator_role)", {"guild_id": guild_id, "channel_id": channel_id, "moderator_role": None})

def update_moderator_role(guild_id : int, role_id : int):
    with conn:
        if get_settings(guild_id, "guild"):
            c.execute("UPDATE settings SET moderator_role = :role_id WHERE guild = :guild_id", {"guild_id": guild_id, "role_id": role_id})
        else:
            c.execute("INSERT INTO settings VALUES (:guild_id, :channel_id, :role_id)", {"guild_id": guild_id, "channel_id": None, "role_id": role_id})



def get_job_info(message_id : int, column : str):
    c.execute("SELECT * FROM jobs WHERE message = :message", {"message": message_id})
    row = c.fetchone()

    if row:
        result = row[column]
    else:
        result = None

    return result


def add_job(guild_id : int, job_message : int, member_id : int, description : str):
    with conn:
        c.execute("INSERT INTO jobs VALUES (:guild_id, :message, :member, :description)", {"guild_id": guild_id,
                                                                                           "message": job_message,
                                                                                           "member": member_id,
                                                                                           "description": description
                                                                                          })

def remove_job(job_message : int):
    with conn:
        c.execute("DELETE FROM jobs WHERE message = :message", {"message": job_message})