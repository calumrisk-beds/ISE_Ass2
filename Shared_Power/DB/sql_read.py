import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.Pool.user import User


class SQLRead:
    """Called to read entries and data in DB."""

    def __init__(self):
        # Required to connect DB
        self.path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()

    def get_user_by_id(self, usr_id):
        """Fetches passed in user from users table in DB."""
        with self.conn:
            self.c.execute("SELECT * FROM users WHERE usr_id = :usr_id", {'usr_id': usr_id})
            return self.c.fetchall()

    def get_tool_by_id(self, tool_id):
        """Fetches passed in tool from tools table in DB."""
        with self.conn:
            self.c.execute("SELECT * FROM tools WHERE tool_id = :tool_id", {'tool_id': tool_id})
            return self.c.fetchall()

    def get_tools_by_uid(self, usr_id):
        """Fetches tools from tools table in DB where passed in User ID matches Tool Owner."""
        with self.conn:
            self.c.execute("SELECT * FROM tools WHERE tool_owner = :usr_id", {'usr_id': usr_id})
            return self.c.fetchall()

    def get_all_tools(self):
        """Fetches all tools from tools table in DB."""
        with self.conn:
            self.c.execute("SELECT * FROM tools")
            return self.c.fetchall()

    def get_booking_by_id(self, booking_id):
        """Fetches passed in booking from bookings table in DB."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE booking_id = :booking_id", {'booking_id': booking_id})
            return self.c.fetchall()

    def get_bookings_by_tid(self, tool_id):
        """Fetches bookings from bookings table in DB where the passed in Tool ID matches Tool ID."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE tool_id = :tool_id", {'tool_id': tool_id})
            return self.c.fetchall()

    def get_bookings_by_booker(self, booked_by):
        """Fetches bookings from bookings table in DB where the passed in User ID matches Booked By."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE booked_by = :booked_by", {'booked_by': booked_by})
            return self.c.fetchall()

    def get_bookings_by_courier(self, courier_id):
        """Fetches bookings from bookings table in DB where the passed in User ID matches Courier ID."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE courier_id = :courier_id", {'courier_id': courier_id})
            return self.c.fetchall()

    def get_open_bookings_by_uid(self, usr_id):
        """Fetches bookings from bookings table in DB where the passed in User ID matches Booked By and
        completed = No."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE booked_by = :usr_id and completed = 'No'", {'usr_id': usr_id})
            return self.c.fetchall()

    def get_closed_bookings_by_uid(self, usr_id):
        """Fetches bookings from bookings table in DB where the passed in User ID matches Booked By and
        completed = Yes."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE booked_by = :usr_id and completed = 'Yes'", {'usr_id': usr_id})
            return self.c.fetchall()

    def get_open_bookings_by_tid(self, tool_id):
        """Fetches bookings from bookings table in DB where the passed in Tool ID matches Tool ID and
        completed = No."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE tool_id = :tool_id and completed = 'No'", {'tool_id': tool_id})
            return self.c.fetchall()

    def get_closed_bookings_by_tid(self, tool_id):
        """Fetches bookings from bookings table in DB where the passed in Tool ID matches Tool ID and
        completed = Yes."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE tool_id = :tool_id and completed = 'Yes'", {'tool_id': tool_id})
            return self.c.fetchall()

    def get_open_bookings_by_courier(self, courier_id):
        """Fetches bookings from bookings table in DB where the passed in User ID matches Courier ID and
        completed = No."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE courier_id = :courier_id and completed = 'No'",
                      {'courier_id': courier_id})
            return self.c.fetchall()

    def get_closed_bookings_by_courier(self, courier_id):
        """Fetches bookings from bookings table in DB where the passed in User ID matches Courier ID and
        completed = Yes."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE courier_id = :courier_id and completed = 'Yes'",
                      {'courier_id': courier_id})
            return self.c.fetchall()

    def get_available_bookings_by_delivery(self):
        """Fetches bookings from bookings table in DB where Courier ID is blank and completed = No."""
        with self.conn:
            self.c.execute("SELECT * FROM bookings WHERE deliv_collect = 'Delivery' and courier_id='' and completed = 'No'")
            return self.c.fetchall()

    def get_cases_by_resolved(self, resolved):
        """Fetches cases from cases table in DB where passed in value for resolved match resolves."""
        with self.conn:
            self.c.execute("SELECT * FROM cases WHERE resolved = :resolved",
                      {'resolved': resolved})
            return self.c.fetchall()

    def get_case_by_id(self, case_id):
        """Fetches case from cases table in DB where passed in Case ID matches Case ID."""
        with self.conn:
            self.c.execute("SELECT * FROM cases WHERE case_id = :case_id",
                           {'case_id': case_id})
            return self.c.fetchall()

    def get_cases_by_bid(self, booking_id):
        """Fetches case from cases table in DB where passed in Booking ID matches Booking ID."""
        with self.conn:
            self.c.execute("SELECT * FROM cases WHERE booking_id = :booking_id",
                           {'booking_id': booking_id})
            return self.c.fetchall()


# For testing purposes
if __name__ == "__main__":
    pass


