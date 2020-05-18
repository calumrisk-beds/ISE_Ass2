import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Classes.user import User


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)
c = conn.cursor()

def update_password(usr_id, new_pwrd):
    with conn:
        c.execute("""UPDATE users SET pwrd = :new_pwrd
                    WHERE usr_id = :usr_id""",
                  {'usr_id': usr_id, 'new_pwrd': new_pwrd})