from tkinter import *
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.DB.sql_read import SQLRead
from Shared_Power.GUI.manage_case import ManageCase


class ViewCases:
    """Displays closed bookings.
        Tk() is passed into master from previous class, allowing main Tkinter window to run.
        The user's ID is passed into uid_token.
        The resolve state is passed into rslv_state."""

    def __init__(self, master, uid_token, rslv_state):
        self.master = master
        self.uid_token = uid_token
        self.rslv_state = rslv_state

        # New window
        self.window = Toplevel()

        # Window title
        self.window.title("Open Cases")

        # Frame packed into window with defined width and height size
        self.frame = Frame(self.window, padx=15, pady=15)
        self.frame.pack(fill=X)  # Packed to fill entire window horizontally

        # Shows open cases:

        self.info = Label(self.frame, text="Select Case")
        self.info.pack()

        # Create Scrollbar
        self.scrlbar = Scrollbar(self.frame, orient=VERTICAL)

        # Create Cases Listbox
        self.cases_lstbx = Listbox(self.frame, width=50, yscrollcommand=self.scrlbar)

        # Configure Scrollbar
        self.scrlbar.config(command=self.cases_lstbx.yview)
        self.scrlbar.pack(side=RIGHT, fill=Y)

        # Pack the Listbox with Scrollbar
        self.cases_lstbx.pack()

        # Call the condition cases by resolve state
        self.cases = SQLRead().get_cases_by_resolved(self.rslv_state)
        for x in self.cases:
            self.lg_id = x[0]
            self.tl_id = x[1]
            self.bkg_id = x[2]
            self.cases_short = "#{}#  Tool ID:{}  Booking ID:{}".format(str(self.lg_id), str(self.tl_id),
                                                                        str(self.bkg_id))
            self.cases_lstbx.insert(END, self.cases_short)

        # Select Case Button
        self.slct_btn = Button(self.frame, text="Select Case", command=self.slct_case)
        self.slct_btn.pack()

    def slct_case(self):
        """Called when a case is selected."""
        # Retrieves selected item and splits the string to retrieve the Case ID
        selected = self.cases_lstbx.get(ANCHOR)
        slcted_case = selected.split('#')[1]

        # Destroy window
        self.window.destroy()

        # Call ManageCase and pass the value of User ID and Log ID
        ManageCase(self.master, self.uid_token, slcted_case)


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    ViewCases(root, 'insurecomp1', 'Yes')
    root.mainloop()
