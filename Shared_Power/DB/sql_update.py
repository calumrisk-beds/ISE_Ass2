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

def update_tool(tl):
    with conn:
        c.execute("""UPDATE tools SET tool_name = :tool_name, descr = :descr, 
                    day_rate = :day_rate, halfd_rate = :halfd_rate, prof_pic = :prof_pic
                    WHERE tool_id = :tool_id""",
                  {'tool_id': tl.tool_id,
                   'tool_owner': tl.tool_owner,
                   'tool_name': tl.tool_name,
                   'descr': tl.descr,
                   'day_rate': tl.day_rate,
                   'halfd_rate': tl.halfd_rate,
                   'prof_pic': tl.prof_pic})

