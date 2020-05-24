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

def get_tools_by_uid(usr_id):
    with conn:
        c.execute("SELECT * FROM tools WHERE tool_owner = :usr_id", {'usr_id': usr_id})
        return c.fetchall()

def get_all_tools():
    with conn:
        c.execute("SELECT * FROM tools")
        return c.fetchall()
    
def get_bookings_by_tid(tool_id):
    with conn:
        c.execute("SELECT * FROM bookings WHERE tool_id = :tool_id", {'tool_id': tool_id})
        return c.fetchall()


if __name__ == "__main__":
    #tools = get_tools_by_uid('test5')

    # for x in tools:
    #    print(x[0])
    
    #alltools = get_all_tools()
    #for x in alltools:
    #    print(x[0])
    tl_bkgs = get_bookings_by_tid(4)
    for x in tl_bkgs:
        print(x[0])


