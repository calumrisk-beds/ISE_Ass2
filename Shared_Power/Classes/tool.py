class Tool:

    def __init__(self, tool_id, tool_owner, tool_name, desc, day_rate, halfd_rate):
        self.tool_id = tool_id
        self.tool_owner = tool_owner  # usr_id of owner.
        self.tool_name = tool_name
        self.desc = desc
        self.day_rate = day_rate
        self.halfd_rate = halfd_rate