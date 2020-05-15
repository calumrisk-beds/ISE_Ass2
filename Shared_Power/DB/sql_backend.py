import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Classes.user import User


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)
c = conn.cursor()


def insert_user(usr):  # Pass in the user you want to create.
    # with conn:  # Eliminates need for commit statement.

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
    conn.commit()

def get_user_by_id(usr_id):
    with conn:
        c.execute("SELECT * FROM users WHERE usr_id = :usr_id", {'usr_id': usr_id})
        return c.fetchall()


def update_password(usr_id, new_pwrd):
    with conn:
        c.execute("""UPDATE users SET pwrd = :new_pwrd
                    WHERE usr_id = :usr_id""",
                  {'usr_id': usr_id, 'new_pwrd': new_pwrd})


def remove_user(usr_id):
    with conn:
        c.execute("DELETE from users WHERE usr_id = :usr_id",
                  {'usr_id': usr_id})


def create_a_user():
    return User(
        input('Username: '),
        input('Password: '),
        input('User Type: '),
        input('First name: '),
        input('Last Name: '),
        input('Address Line 1: '),
        input('Address Line 2: '),
        input('Address Line 3: '),
        input('Address Line 4: '),
        input('Post Code: '),
        input('Telephone No: '),
        0)


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
    pass
