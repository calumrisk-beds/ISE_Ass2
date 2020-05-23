class Booking:
    def __init__(self, booking_id, tool_id, booked_by, start_time, end_time, deliv_collect):
        self.booking_id = booking_id
        self.tool_id = tool_id
        self.booked_by = booked_by  # usr_id of user who books tool.
        self.start_time = start_time
        self.end_time = end_time
        self.deliv_collect = deliv_collect  # Delivery or collection.
