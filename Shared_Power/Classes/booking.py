class Booking:
    def __init__(self, booking_id, tool_id, booked_by, start_time, end_time,
                 deliv_collect, courier_id, completed, days_late):
        self.booking_id = booking_id
        self.tool_id = tool_id
        self.booked_by = booked_by  # usr_id of user who books tool
        self.start_time = start_time
        self.end_time = end_time
        self.deliv_collect = deliv_collect  # delivery or collection
        self.courier_id = courier_id  # usr_id of dispatch rider if required
        self.completed = completed
        self.days_late = days_late
