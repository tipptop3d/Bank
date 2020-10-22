import sqlite3

conn = sqlite3.connect('bank.db')

conn.row_factory = sqlite3.Row

c = conn.cursor()

def get_money(member_id):
    c.execute(f"SELECT * FROM money WHERE member=:member_id", {"member_id": member_id})
    
    row = c.fetchone()

    if row:
        money = row["amount"]
    else:
        money = 0

    return money

def update_money(member_id, amount):
    c.execute("SELECT * FROM money WHERE member=:member_id", {"member_id": member_id})

    with conn:
        if c.fetchone():
            c.execute("UPDATE money SET amount = :amount WHERE member = :member_id", {"member_id": member_id, "amount": amount})
        else:
            c.execute("INSERT INTO money VALUES (:member_id, :amount)", {"member_id": member_id, "amount": amount})

def delete_money_entry(member_id):
    c.execute(f"DELETE FROM money WHERE member=:member_id", {"member_id": member_id})
