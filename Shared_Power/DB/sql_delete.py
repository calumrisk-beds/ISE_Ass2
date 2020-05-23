import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Classes.user import User


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)
c = conn.cursor()


def remove_user(usr_id):
    with conn:
        c.execute("DELETE from users WHERE usr_id = :usr_id",
                  {'usr_id': usr_id})

def drop_table(tbl_name):
    with conn:
        c.execute("DROP TABLE {}".format(tbl_name))


if __name__ == "__main__":
    # drop_table('tools')
    pass
