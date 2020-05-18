import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Classes.user import User


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)
c = conn.cursor()


def insert_user(usr):  # Pass in the user you want to create.
    with conn:  # Eliminates need for commit statement.
        c.execute("""INSERT INTO users VALUES (
                           :usr_id, :pwrd, :usr_type, :first_name,
                           :last_name, :add1, :add2, :add3,
                           :add4, :post_code, :tel_no, :wallet)""",
                  {'usr_id': usr.usr_id,
                   'pwrd': usr.pwrd,
                   'usr_type': usr.usr_type,
                   'first_name': usr.first_name,
                   'last_name': usr.last_name,
                   'add1': usr.add1,
                   'add2': usr.add2,
                   'add3': usr.add3,
                   'add4': usr.add4,
                   'post_code': usr.post_code,
                   'tel_no': usr.tel_no,
                   'wallet': usr.wallet})


def insert_tool(tl):  # Pass in the tool you want to create.
    with conn:
        c.execute("""INSERT INTO tools VALUES (
                           NULL, :tool_owner, :tool_name, :descr,
                           :day_rate, :halfd_rate, :prof_pic)""",
                  {'tool_id': tl.tool_id,
                   'tool_owner': tl.tool_owner,
                   'tool_name': tl.tool_name,
                   'descr': tl.descr,
                   'day_rate': tl.day_rate,
                   'halfd_rate': tl.halfd_rate,
                   'prof_pic': tl.prof_pic})


def create_users_table():
    with conn:
        c.execute("""CREATE TABLE users (
                    usr_id TEXT PRIMARY KEY,
                    pwrd TEXT,
                    usr_type text,
                    first_name TEXT,
                    last_name TEXT,
                    add1 TEXT,
                    add2 TEXT,
                    add3 TEXT,
                    add4 TEXT,
                    post_code TEXT,
                    tel_no TEXT,
                    wallet REAL 
                )""")


def create_tools_table():
    with conn:
        c.execute("""CREATE TABLE tools (
                    tool_id INTEGER PRIMARY KEY,
                    tool_owner TEXT,
                    tool_name TEXT,
                    descr TEXT,
                    day_rate REAL,
                    halfd_rate REAL,
                    prof_pic BLOB           
                )""")


if __name__ == "__main__":
    # create_users_table()
    # create_sample_user()
    # sample_select()
    # create_sample_user_2()
    # create_sample_user_3()
    # sample_select_2()
    # sample_select_3()
    # usr = create_a_user()
    # insert_user(usr)
    # update_password('lukeskywalker', 'sabre')
    # remove_user('Test6')
    # get_user_by_id('test2')
    # create_users_table()
    # create_tools_table()
    pass
