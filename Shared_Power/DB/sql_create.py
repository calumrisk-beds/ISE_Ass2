import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Pool.user import User
from Shared_Power.Pool.booking import Booking


class SQLCreate:
    """Called to create new entries and data in DB."""

    def __init__(self):
        # Required to connect DB
        self.path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()

    def insert_user(self, usr):
        """Creates new user by passing in a User object."""
        with self.conn:  # Eliminates need for commit statement.
            self.c.execute("""INSERT INTO users VALUES (
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

    def insert_tool(self, tl):
        """Creates new tool by passing through a Tool object."""
        with self.conn:
            self.c.execute("""INSERT INTO tools VALUES (
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

    def insert_booking(self, bkg):
        """Creates new booking by passing through a Booking object."""
        with self.conn:
            self.c.execute("""INSERT INTO bookings VALUES (
                                NULL, :tool_id, :booked_by, :start_time, :end_time, 
                                :deliv_collect, :courier_id, :completed, :days_late)""",
                           {'booking_id': bkg.booking_id,
                            'tool_id': bkg.tool_id,
                            'booked_by': bkg.booked_by,
                            'start_time': bkg.start_time,
                            'end_time': bkg.end_time,
                            'deliv_collect': bkg.deliv_collect,
                            'courier_id': bkg.courier_id,
                            'completed': bkg.completed,
                            'days_late': bkg.days_late})

    def insert_case(self, case):
        """Creates new case by passing through a Case object."""
        with self.conn:
            self.c.execute("""INSERT INTO cases VALUES (
                                NULL, :tool_id, :booking_id, :notes, :photo1, :photo2, 
                                :photo3, :photo4, :at_fault, :damage_charge, :resolved)""",
                      {'case_id': case.case_id,
                       'tool_id': case.tool_id,
                       'booking_id': case.booking_id,
                       'notes': case.notes,
                       'photo1': case.photo1,
                       'photo2': case.photo2,
                       'photo3': case.photo3,
                       'photo4': case.photo4,
                       'at_fault': case.at_fault,
                       'damage_charge': case.damage_charge,
                       'resolved': case.resolved})

    def create_users_table(self):
        """Creates users table if it does not exist."""
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS users (
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

    def create_tools_table(self):
        """Creates tools table if it does not exist."""
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS tools (
                        tool_id INTEGER PRIMARY KEY,
                        tool_owner TEXT,
                        tool_name TEXT,
                        descr TEXT,
                        day_rate REAL,
                        halfd_rate REAL,
                        prof_pic BLOB,
                        repair_status TEXT           
                    )""")

    def create_bookings_table(self):
        """Creates bookings table if it does not exist."""
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS bookings (
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

    def create_cases_table(self):
        """Creates cases table if it does not exist."""
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS cases (
                        case_id INTEGER PRIMARY KEY,
                        tool_id INTEGER,
                        booking_id INTEGER,
                        notes TEXT,
                        photo1 BLOB,
                        photo2 BLOB,
                        photo3 BLOB,
                        photo4 BLOB,
                        at_fault TEXT,
                        damage_charge REAL,
                        resolved TEXT
                        )""")


# For testing purposes
if __name__ == "__main__":
    # create_users_table()
    #usr = User(usr_id='insurecomp1', pwrd='insure', usr_type="Insurance Company",
    #           first_name='', last_name='', add1="Insure Ltd", add2="1 Street Avenue", add3="Bedford",
    #           add4="Bedfordshire", post_code="MK40 1GH", tel_no='01234555556')
    # insert_user(usr)

    bkg = Booking(booking_id='', tool_id=1, booked_by='tu2', start_time='4/20/20:ALL DAY', end_time='4/21/20:ALL DAY',
                   deliv_collect='Collection', courier_id='', completed='No', days_late=0)
    SQLCreate().insert_booking(bkg)
    pass

