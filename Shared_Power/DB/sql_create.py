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
                           :add4, :post_code, :tel_no)""",
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
                   'tel_no': usr.tel_no})


def insert_tool(tl):  # Pass in the tool you want to create.
    with conn:
        c.execute("""INSERT INTO tools VALUES (
                           NULL, :tool_owner, :tool_name, :descr,
                           :day_rate, :halfd_rate, :prof_pic, :repair_status)""",
                  {'tool_id': tl.tool_id,
                   'tool_owner': tl.tool_owner,
                   'tool_name': tl.tool_name,
                   'descr': tl.descr,
                   'day_rate': tl.day_rate,
                   'halfd_rate': tl.halfd_rate,
                   'prof_pic': tl.prof_pic,
                   'repair_status': tl.repair_status})


def insert_booking(bkg):
    with conn:
        c.execute("""INSERT INTO bookings VALUES (
                            NULL, :tool_id, :booked_by, :start_time,
                            :end_time, :deliv_collect, :courier_id, :completed, :days_late)""",
                  {'booking_id': bkg.booking_id,
                   'tool_id': bkg.tool_id,
                   'booked_by': bkg.booked_by,
                   'start_time': bkg.start_time,
                   'end_time': bkg.end_time,
                   'deliv_collect': bkg.deliv_collect,
                   'courier_id': bkg.courier_id,
                   'completed': bkg.completed,
                   'days_late': bkg.days_late})


def insert_condition_log(clog):
    with conn:
        c.execute("""INSERT INTO condition_log VALUES (
                            NULL, :tool_id, :booking_id, :notes,
                            :photo1, :photo2, :photo3, :photo4)""",
                  {'log_id': clog.log_id,
                   'tool_id': clog.tool_id,
                   'booking_id': clog.booking_id,
                   'notes': clog.notes,
                   'photo1': clog.photo1,
                   'photo2': clog.photo2,
                   'photo3': clog.photo3,
                   'photo4': clog.photo4})


def create_users_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
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
                    tel_no TEXT 
                )""")


def create_tools_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS tools (
                    tool_id INTEGER PRIMARY KEY,
                    tool_owner TEXT,
                    tool_name TEXT,
                    descr TEXT,
                    day_rate REAL,
                    halfd_rate REAL,
                    prof_pic BLOB,
                    repair_status TEXT           
                )""")


def create_bookings_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY,
                    tool_id INTEGER,
                    booked_by TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    deliv_collect TEXT,
                    courier_id TEXT,
                    completed TEXT,
                    days_late INTEGER
                    )""")


def create_condition_log_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS condition_log (
                    log_id INTEGER PRIMARY KEY,
                    tool_id INTEGER,
                    booking_id INTEGER,
                    notes TEXT,
                    photo1 BLOB,
                    photo2 BLOB,
                    photo3 BLOB,
                    photo4 BLOB
                    )""")


def create_deliveries_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS deliveries (
                    deliv_id INTEGER PRIMARY KEY,
                    booking_id INTEGER,
                    available TEXT,
                    assigned_to TEXT,
                    completed TEXT
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
    # create_bookings_table()
    # create_condition_log_table()
    pass
