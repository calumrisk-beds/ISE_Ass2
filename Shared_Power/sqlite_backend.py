# sqlite_backend.py

import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
from Shared_Power import mvc_exceptions as mvc_exc

DB_name = 'SharedPowerDB'


def connect_to_db(db=None):
    """Connect to a sqlite DB. Create the database if there isn't one yet.

    Open a connection to a SQLite DB (either a DB file or an in-memory DB).
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    db : str
        database name (without .db extension). If None, create an In-Memory DB.

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection


# TODO: use this decorator to wrap commit/rollback in a try/except block ?
# see http://www.kylev.com/2009/05/22/python-decorators-and-database-idioms/
def connect(func):
    """Decorator to (re)open a sqlite database connection when needed.

    A database connection must be open when we want to perform a database query
    but we are in one of the following situations:
    1) there is no connection
    2) the connection is closed

    Parameters
    ----------
    func : function
        function which performs the database query

    Returns
    -------
    inner func : function
    """

    def inner_func(conn, *args, **kwargs):
        try:
            # I don't know if this is the simplest and fastest query to try
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)

    return inner_func


def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum())

@connect
def create_users_table(conn, table_name):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (usr_id TEXT PRIMARY KEY,' \
          'pwrd TEXT, usr_type TEXT,' \
          'first_name TEXT, last_name TEXT,' \
          'add1 TEXT, add2 TEXT, add3 TEXT, add4 TEXT, post_code TEXT,' \
          'tel_no TEXT)'.format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)
@connect
def create_tools_table(conn, table_name):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (tool_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'tool_name TEXT, desc TEXT,' \
          'owner TEXT, day_rate MONEY, halfd_rate MONEY' \
          'condition TEXT, photo VARBINARY(MAX),'.format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)
@connect
def create_bookings_table(conn, table_name):
    table_name = scrub(table_name)
    sql = 'CREATE TABLE {} (booking_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'tool_hired TEXT, hired_by TEXT,' \
          'start_time DATETIME, end_time DATETIME,' \
          'del_col TEXT, last_name TEXT)'.format(table_name)
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)

@connect
def insert_one_users(
        conn, usr_id, pwrd, usr_type, first_name, last_name,
        add1, add2, add3, add4, post_code, tel_no, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('usr_id', 'pwrd', 'usr_type', 'first_name', 'last_name', \
           'add1', 'add2', 'add3', 'add4', 'post_code', 'tel_no') \
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)
    try:
        conn.execute(sql, (
            usr_id, pwrd, usr_type, first_name, last_name,
            add1, add2, add3, add4, post_code, tel_no))
        conn.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '{}: "{}" already stored in table "{}"'.format(e, usr_id, table_name))


@connect
def insert_users(conn, items, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('usr_id', 'pwrd', 'usr_type', 'first_name', 'last_name', \
           'add1', 'add2', 'add3', 'add4', 'post_code', 'tel_no') \
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)
    entries = list()
    for x in items:
        entries.append((x['usr_id'], x['pwrd'], x['usr_type'], x['first_name'],
                        x['last_name'], x['add1'], x['add2'],
                        x['add3'], x['add4'], x['post_code'], x['tel_no']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [x['usr_id'] for x in items], table_name))

@connect
def insert_tools(conn, items, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('tool_name', 'desc', 'owner', 'day_rate', \
           'halfd_rate', 'condition', 'photo') \
           VALUES (?, ?, ?, ?, ?, ?, ?)".format(table_name)
    entries = list()
    for x in items:
        entries.append((x['tool_name'], x['desc'], x['owner'],
                        x['day_rate'], x['halfd_rate'], x['condition'],
                        x['photo']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [x['tool_name'] for x in items], table_name))

@connect
def insert_bookings(conn, items, table_name):
    table_name = scrub(table_name)
    sql = "INSERT INTO {} ('tool_hired', 'hired_by', 'start_time', \
           'end_time', 'del_col') \
           VALUES (?, ?, ?, ?, ?)".format(table_name)
    entries = list()
    for x in items:
        entries.append((x['tool_hired'], x['hired_by'], x['start_time'],
                        x['end_time'], x['del_col']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [x['tool_hired'] for x in items], table_name))

def tuple_to_dict_users(mytuple):
    mydict = dict()
    mydict['usr_id'] = mytuple[0]
    mydict['pwrd'] = mytuple[1]
    mydict['usr_type'] = mytuple[2]
    mydict['first_name'] = mytuple[3]
    mydict['last_name'] = mytuple[4]
    mydict['add1'] = mytuple[5]
    mydict['add2'] = mytuple[6]
    mydict['add3'] = mytuple[7]
    mydict['add4'] = mytuple[8]
    mydict['post_code'] = mytuple[9]
    mydict['tel_no'] = mytuple[10]
    return mydict

def tuple_to_dict_tools(mytuple):
    mydict = dict()
    mydict['tool_id'] = mytuple[0]
    mydict['tool_name'] = mytuple[1]
    mydict['desc'] = mytuple[2]
    mydict['owner'] = mytuple[3]
    mydict['day_rate'] = mytuple[4]
    mydict['halfd_rate'] = mytuple[5]
    mydict['condition'] = mytuple[6]
    mydict['photo'] = mytuple[7]
    return mydict

def tuple_to_dict_bookings(mytuple):
    mydict = dict()
    mydict['booking_id'] = mytuple[0]
    mydict['tool_hired'] = mytuple[1]
    mydict['hired_by'] = mytuple[2]
    mydict['start_date'] = mytuple[3]
    mydict['end_time'] = mytuple[4]
    mydict['del_col'] = mytuple[5]
    return mydict

@connect
def select_one_users(conn, item_name, table_name):
    table_name = scrub(table_name)
    item_name = scrub(item_name)
    sql = 'SELECT * FROM {} WHERE usr_id="{}"'.format(table_name, item_name)
    c = conn.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict_users(result)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read {} because it\'s not stored in table {}'
            .format(item_name, table_name))


@connect
def select_all_users(conn, table_name):
    table_name = scrub(table_name)
    sql = 'SELECT * FROM {}'.format(table_name)
    c = conn.execute(sql)
    results = c.fetchall()
    return list(map(lambda x: tuple_to_dict_users(x), results))


@connect
def select_one_tools(conn, item_name, table_name):
    table_name = scrub(table_name)
    item_name = scrub(item_name)
    sql = 'SELECT * FROM {} WHERE tool_id="{}"'.format(table_name, item_name)
    c = conn.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict_tools(result)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(item_name, table_name))


@connect
def select_all_tools(conn, table_name):
    table_name = scrub(table_name)
    sql = 'SELECT * FROM {}'.format(table_name)
    c = conn.execute(sql)
    results = c.fetchall()
    return list(map(lambda x: tuple_to_dict_tools(x), results))


@connect
def select_one_bookings(conn, item_name, table_name):
    table_name = scrub(table_name)
    item_name = scrub(item_name)
    sql = 'SELECT * FROM {} WHERE booking_id="{}"'.format(table_name, item_name)
    c = conn.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict_bookings(result)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(item_name, table_name))


@connect
def select_all_bookings(conn, table_name):
    table_name = scrub(table_name)
    sql = 'SELECT * FROM {}'.format(table_name)
    c = conn.execute(sql)
    results = c.fetchall()
    return list(map(lambda x: tuple_to_dict_bookings(x), results))


@connect
def update_one_users(
        conn, usr_id, pwrd, usr_type, first_name, last_name,
        add1, add2, add3, add4, post_code, tel_no, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE usr_id=? LIMIT 1)' \
        .format(table_name)
    sql_update = 'UPDATE {} SET pwrd=?, usr_type=?, first_name=?, last_name=?, add1=?, add2=?, add3=?, add4=?, post_code=?, tel_no=? WHERE usr_id=?'\
        .format(table_name)
    c = conn.execute(sql_check, (usr_id,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_update, (pwrd, usr_type, first_name, last_name, add1, add2, add3, add4, post_code, tel_no, usr_id))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'
            .format(usr_id, table_name))

@connect
def update_one_tools(conn, tool_id, tool_name, desc, owner, day_rate, halfd_rate, condition, photo, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE tool_id=? LIMIT 1)' \
        .format(table_name)
    sql_update = 'UPDATE {} SET tool_name=?, desc, owner=?, day_rate=?, halfd_rate=?, condition=?, photo=? WHERE tool_id=?' \
        .format(table_name)
    c = conn.execute(sql_check, (tool_id,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_update, (tool_name, desc, owner, day_rate, halfd_rate, condition, photo))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'
            .format(tool_id, table_name))


@connect
def update_one_bookings(conn, booking_id, tool_hired, hired_by, start_time, end_time, del_col, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE booking_id=? LIMIT 1)' \
        .format(table_name)
    sql_update = 'UPDATE {} SET booking_id=?, tool_hired=?, hired_by=?, start_time=?, end_time=?, del_col=? WHERE booking_id=?' \
        .format(table_name)
    c = conn.execute(sql_check, (booking_id,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_update, (tool_hired, hired_by, start_time, end_time, del_col))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table "{}"'
            .format(booking_id, table_name))


@connect
def delete_one_users(conn, usr_id, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE usr_id=? LIMIT 1)' \
        .format(table_name)
    table_name = scrub(table_name)
    sql_delete = 'DELETE FROM {} WHERE usr_id=?'.format(table_name)
    c = conn.execute(sql_check, (usr_id,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_delete, (usr_id,))  # we need the comma
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'
                .format(usr_id, table_name))


@connect
def delete_one_tools(conn, tool_id, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE tool_id=? LIMIT 1)' \
        .format(table_name)
    table_name = scrub(table_name)
    sql_delete = 'DELETE FROM {} WHERE tool_id=?'.format(table_name)
    c = conn.execute(sql_check, (tool_id,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_delete, (tool_id,))  # we need the comma
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'
                .format(tool_id, table_name))


@connect
def delete_one_bookings(conn, booking_id, table_name):
    table_name = scrub(table_name)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE booking_id=? LIMIT 1)' \
        .format(table_name)
    table_name = scrub(table_name)
    sql_delete = 'DELETE FROM {} WHERE booking_id=?'.format(table_name)
    c = conn.execute(sql_check, (booking_id,))  # we need the comma
    result = c.fetchone()
    if result[0]:
        c.execute(sql_delete, (booking_id,))  # we need the comma
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t delete "{}" because it\'s not stored in table "{}"'
                .format(booking_id, table_name))


def main_users():

    table_name = 'users'
    # conn = connect_to_db()  # in-memory database
    conn = connect_to_db(DB_name)  # physical database (i.e. a .db file)

    create_users_table(conn, table_name)

    my_items = [
        {'usr_id': 'joebloggs', 'pwrd': 'secure', 'usr_type': 'Tool Owner',
         'first_name': 'Joe', 'last_name': 'Bloggs', 'add1': 'Putteridge Bury',
         'add2': 'Hitchin Rd', 'add3': 'Luton', 'add4': 'Bedfordshire',
         'post_code': 'LU2 8LE', 'tel_no': '01582 489069'},
        {'usr_id': 'john.smith', 'pwrd': 'password', 'usr_type': 'Tool User',
         'first_name': 'John', 'last_name': 'Smith', 'add1': 'Vicarage St',
         'add2': '', 'add3': 'Luton', 'add4': '',
         'post_code': 'LU1 3JU', 'tel_no': '01234 400400'},
        {'usr_id': 'admin', 'pwrd': 'admin', 'usr_type': 'Sys Admin',
         'first_name': 'System', 'last_name': 'Administrator', 'add1': '',
         'add2': '', 'add3': '', 'add4': '',
         'post_code': '', 'tel_no': ''},
    ]

    # CREATE
    insert_users(conn, my_items, table_name='users')
    # not using: insert_one(conn, 'beer', price=2.0, quantity=5, table_name='items')
    # if we try to insert an object already stored we get an ItemAlreadyStored
    # exception
    # insert_one(conn, 'milk', price=1.0, quantity=3, table_name='items')

    # READ
    print('SELECT joebloggs')
    # print(select_one(conn, 'milk', table_name='items'))
    print('SELECT all')
    print(select_all_users(conn, table_name='users'))
    # if we try to select an object not stored we get an ItemNotStored exception
    # print(select_one(conn, 'pizza', table_name='items'))

    # conn.close()  # the decorator @connect will reopen the connection

    # UPDATE
    print('UPDATE joebloggs, SELECT joebloggs')
    update_one_users(
        conn, usr_id='joebloggs', pwrd='securepass', usr_type='Tool Owner',
        first_name='Joseph', last_name='Bloggs', add1='Putteridge Bury',
        add2='Hitchin Rd', add3='Luton', add4='Bedfordshire',
        post_code='LU2 8LE', tel_no='01582 489069', table_name='users')
    print(select_one_users(conn, item_name='joebloggs', table_name='users'))
    # if we try to update an object not stored we get an ItemNotStored exception
    # print('UPDATE pizza')
    # update_one(conn, 'pizza', price=1.5, quantity=5, table_name='items')

    # DELETE
    print('DELETE admin, SELECT all')
    delete_one_users(conn, 'admin', table_name='users')
    print(select_all_users(conn, table_name='users'))
    # if we try to delete an object not stored we get an ItemNotStored exception
    # print('DELETE fish')
    # delete_one(conn, 'fish', table_name='items')

    # save (commit) the changes
    # conn.commit()

    # close connection
    conn.close()


if __name__ == '__main__':
    main_users()

# conn = connect_to_db()  # in-memory database
conn = connect_to_db(DB_name)  # physical database (i.e. a .db file)
