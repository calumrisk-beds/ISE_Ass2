class Case:
    def __init__(self, case_id, tool_id, booking_id, notes, photo1, photo2, photo3, photo4,
                 at_fault, damage_charge,  resolved):
        self.case_id = case_id
        self.tool_id = tool_id
        self.booking_id = booking_id
        self.notes = notes
        self.photo1 = photo1
        self.photo2 = photo2
        self.photo3 = photo3
        self.photo4 = photo4
        self.at_fault = at_fault  # User ID of person at fault
        self.damage_charge = damage_charge
        self.resolved = resolved
