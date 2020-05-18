import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Classes.user import User


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)
c = conn.cursor()


def get_user_by_id(usr_id):
    with conn:
        c.execute("SELECT * FROM users WHERE usr_id = :usr_id", {'usr_id': usr_id})
        return c.fetchall()


def get_tool_by_id(tool_id):
    with conn:
        c.execute("SELECT * FROM tools WHERE tool_id = :tool_id", {'tool_id': tool_id})
        return c.fetchall()

