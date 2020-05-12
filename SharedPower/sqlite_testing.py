import sqlite3
from SharedPower.test_users  import User

db = 'shared_power.db'

conn = sqlite3.connect(db)
c = conn.cursor()

def create_users_table():
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
                wallet integer 
            )""")
    conn.commit()
    conn.close()


def create_sample_user_1():
    c.execute("""INSERT INTO users VALUES (
                'joesbloggs',
                'secure',
                'tool_owner',
                'Joe',
                'Bloggs',
                '1 Place',
                'Road',
                'Luton',
                'Beds',
                'LU3 3AA',
                '0777777777',
                0          
            )""")
    conn.commit()
    conn.close()

def create_sample_user_2():
    usr = User(
        'johnsmith',
        'pass',
        'tool_user',
        'John',
        'Smith',
        'Building',
        'Street',
        'Milton Keynes',
        'Bucks',
        'MK1 1SW',
        '01234567890',
        100)

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (usr.usr_id, usr.pwrd, usr.usr_type, usr.first_name,
               usr.last_name, usr.add1, usr.add2, usr.add3,
               usr.add4, usr.post_code, usr.tel_no, usr.wallet))

    conn.commit()
    conn.close()

def create_sample_user_3():
    usr = User(
        'marywilson',
        'strong',
        'dispatch_rider',
        'Mary',
        'Wilson',
        'Craggy House',
        'Clare Street',
        '',
        'Belfast',
        'BE1 2ZX',
        '0800800800',
        50
    )

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
    conn.close()


def sample_select_1():
    c.execute("SELECT * FROM users WHERE usr_id='joesbloggs'")
    print(c.fetchone())
    conn.commit()
    conn.close()


def sample_select_2():
    c.execute("SELECT * FROM users WHERE usr_id=?", ('johnsmith',))
    print(c.fetchone())
    conn.commit()
    conn.close()


def sample_select_3():
    c.execute("SELECT * FROM users WHERE usr_id=:usr_id", {'usr_id': 'marywilson'})
    print(c.fetchone())
    conn.commit()
    conn.close()


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


def get_user_by_id(usr_id):
    c.execute("SELECT * FROM users WHERE usr_id=:usr_id", {'usr_id': usr_id})
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
    #create_users_table()
    #create_sample_user()
    #sample_select()
    #create_sample_user_2()
    #create_sample_user_3()
    #sample_select_2()
    #sample_select_3()
    #usr = create_a_user()
    #insert_user(usr)
    #update_password('lukeskywalker', 'sabre')
    #remove_user('lukeskywalker')

