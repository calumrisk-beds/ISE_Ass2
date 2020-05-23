class Delivery:
    def __init__(self, deliv_id, booking_id, available, assigned_to):
        self.deliv_id = deliv_id
        self.booking_id = booking_id
        self.available = available
        self.assigned_to = assigned_to  # usr_id of dispatch_rider.
