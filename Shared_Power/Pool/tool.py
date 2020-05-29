class Tool:

    def __init__(self, tool_id, tool_owner, tool_name, descr, day_rate, halfd_rate, prof_pic, repair_status):
        self.tool_id = tool_id
        self.tool_owner = tool_owner  # usr_id of owner.
        self.tool_name = tool_name
        self.descr = descr
        self.day_rate = day_rate
        self.halfd_rate = halfd_rate
        self.prof_pic = prof_pic
        self.repair_status = repair_status
