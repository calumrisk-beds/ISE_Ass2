import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Pool.user import User


class SQLDelete:
    """Called to delete entries and data in DB."""

    def __init__(self):
        # Required to connect DB
        self.path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()

    def remove_user(self, usr_id):
        """Removes passed in user from users table in DB."""
        with self.conn:
            self.c.execute("DELETE from users WHERE usr_id = :usr_id",
                      {'usr_id': usr_id})

    def remove_booking(self, booking_id):
        """Removes passed in booking from bookings table in DB."""
        with self.conn:
            self.c.execute("DELETE from bookings WHERE booking_id = :booking_id",
                      {'booking_id': booking_id})

    def drop_table(self, tbl_name):
        """Deletes table name passed in."""
        with self.conn:
            self.c.execute("DROP TABLE {}".format(tbl_name))


# For testing purposes
if __name__ == "__main__":
    # SQLDelete().drop_table('cases')
    pass
