from tkinter import *
from Shared_Power.GUI.manage_booking import ManageBooking
from Shared_Power.DB.sql_read import SQLRead



class ClosedBookings:
    """Displays closed bookings.
        Tk() is passed into master from previous class, allowing main Tkinter window to run.
        The user's ID is passed into uid_token.
        The selected tool is passed into slcted_tl."""

    def __init__(self, master, uid_token, slcted_tl):
        self.master = master
        self.uid_token = uid_token
        self.slcted_tl = slcted_tl

        # New window
        self.window = Toplevel()

        # Window title
        self.window.title("My Closed Bookings")

        # Frame packed into window with defined width and height size
        self.frame = Frame(self.window, padx=15, pady=15)
        self.frame.pack(fill=X)  # Packed to fill entire window horizontally

        # Shows closed bookings:

        self.closed_bkgs_lbl = Label(self.frame, text="ClosedBookings")
        self.closed_bkgs_lbl.pack()

        # Create Scrollbar
        self.bkgs_scrlbar = Scrollbar(self.frame, orient=VERTICAL)

        # Create Bookings Listbox
        self.bkgs_lstbx = Listbox(self.frame, width=50, yscrollcommand=self.bkgs_scrlbar)

        # Configure Scrollbar
        self.bkgs_scrlbar.config(command=self.bkgs_lstbx.yview)
        self.bkgs_scrlbar.pack(side=RIGHT, fill=Y)

        # Pack the Listbox with Scrollbar
        self.bkgs_lstbx.pack(fill=X)

        # Call the user from the DB and check their user type
        self.this_usr = SQLRead().get_user_by_id(self.uid_token)
        self.usr_type = self.this_usr[0][2]

        # Call the user's or tool's bookings depending on user type
        if self.usr_type == "Tool Owner":
            self.my_closed_bkgs = SQLRead().get_closed_bookings_by_tid(self.slcted_tl)
        if self.usr_type == "Tool User":
            self.my_closed_bkgs = SQLRead().get_closed_bookings_by_uid(self.uid_token)
        if self.usr_type == "Dispatch Rider":
            self.my_closed_bkgs = SQLRead().get_closed_bookings_by_courier(self.uid_token)

        # Loops through each booking and plots a readable string for the listbox
        for x in self.my_closed_bkgs:
            self.bkg_id = x[0]
            self.bkg_tl = x[1]
            self.bkg_start = x[3]
            self.bkg_end = x[4]
            self.bkg_dc = x[5]
            self.bkgs_short = "#{}#  Tool ID: {}  {}  to  {}  ({})".format(str(self.bkg_id), str(self.bkg_tl),
                                                                           str(self.bkg_start),
                                                                           str(self.bkg_end), str(self.bkg_dc))
            self.bkgs_lstbx.insert(END, self.bkgs_short)

        # Select Booking Button
        self.slct_bkg_btn = Button(self.frame, text="Select", command=self.my_closed_bkgs)
        self.slct_bkg_btn.pack()

    def select_bkg(self):
        """Called when a tool is selected."""
        # Retrieves selected item and splits the string to retrieve the Booking ID
        selected = self.bkgs_lstbx.get(ANCHOR)
        selected_bid = selected.split('#')[1]

        # Destroy window
        self.window.destroy()

        # Call ManageBooking and pass the value of User ID and Booking ID
        ManageBooking(self.master, self.uid_token, selected_bid)