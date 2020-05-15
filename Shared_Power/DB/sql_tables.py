import sqlite3
from os.path import join, dirname, abspath

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)
c = conn.cursor()

def create_users_table():
    with conn:
        c.execute("""CREATE TABLE users (
                    usr_id text PRIMARY KEY,
                    pwrd text,
                    usr_type text,
                    first_name text,
                    last_name text,
                    add1 text,
                    add2 text,
                    add3 text,
                    add4 text,
                    post_code text,
                    tel_no text,
                    wallet real 
                )""")


if __name__ == "__main__":
    create_users_table()
