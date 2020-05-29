import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Pool.user import User

class SQLUpdate:
    """Called to update entries and data in DB."""

    def __init__(self):
        # Required to connect DB
        self.path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()

    def update_password(self, usr_id, new_pwrd):
        """Updates user password field from users table in DB with new passed in password
        where passed in User ID matches User ID."""
        with self.conn:
            self.c.execute("""UPDATE users SET pwrd = :new_pwrd
                        WHERE usr_id = :usr_id""",
                      {'usr_id': usr_id, 'new_pwrd': new_pwrd})

    def update_tool(self, tl):
        """Updates tool from tools table by passing in a Tool object."""
        with self.conn:
            self.c.execute("""UPDATE tools SET tool_name = :tool_name, descr = :descr, 
                        day_rate = :day_rate, halfd_rate = :halfd_rate, prof_pic = :prof_pic
                        WHERE tool_id = :tool_id""",
                      {'tool_id': tl.tool_id,
                       'tool_owner': tl.tool_owner,
                       'tool_name': tl.tool_name,
                       'descr': tl.descr,
                       'day_rate': tl.day_rate,
                       'halfd_rate': tl.halfd_rate,
                       'prof_pic': tl.prof_pic})

    def update_case(self, case):
        """Updates case from cases table by passing in a Case object."""
        with self.conn:
            self.c.execute("""UPDATE cases SET
                                tool_id = :tool_id, booking_id = :booking_id, notes = :notes, 
                                photo1 = :photo1, photo2 = :photo2, photo3 = :photo3, photo4 = :photo4, 
                                at_fault = :at_fault, damage_charge = :damage_charge, resolved = :resolved
                                WHERE case_id = :case_id""",
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

    def assign_courier(self, booking_id, courier_id):
        """Updates Courier ID field from bookings table in DB with passed in User ID
        where passed in Booking ID matches Booking ID."""
        with self.conn:
            self.c.execute("""UPDATE bookings SET courier_id = :courier_id
                                    WHERE booking_id = :booking_id""",
                        {'booking_id': booking_id, 'courier_id': courier_id})

    def add_table_column(self, table_name, column_name, data_type):
        """Adds column to passed in table name with name of passed in column name and
        with the data type of the passed in data type."""
        with self.conn:
            self.c.execute("ALTER TABLE {} ADD {} {}".format(table_name, column_name, data_type))

    def complete_booking(self, booking_id, completed, days_late):
        """Updates completed and days_late field from bookings table in DB with new passed in values
        where passed in Booking ID matches Booking ID."""
        with self.conn:
            self.c.execute("""UPDATE bookings SET completed = :completed, days_late = :days_late
                                WHERE booking_id = :booking_id""",
                        {'booking_id': booking_id, 'completed': completed, 'days_late': days_late})


# For testing purposes
if __name__ == "__main__":
    pass

