from tkinter import *
from tkcalendar import *
import datetime
from datetime import date
from Shared_Power.DB.sql_create import SQLCreate
from Shared_Power.DB.sql_read import SQLRead
from Shared_Power.Pool.booking import Booking


class BookTool:
    """Called to book a tool.
        Tk() is passed into master from previous class, allowing main Tkinter window to run.
        The user's ID is passed into uid_token.
        The selected tool is passed into slcted_tl."""

    def __init__(self, master, uid_token, slcted_tl):
        self.master = master
        self.uid_token = uid_token
        self.slcted_tl = slcted_tl

        # New window
        self.window = Toplevel()

        # Defining window title
        self.window.title("Book Tool")

        # Uses a main frame for other frames to be packed into
        self.mainframe = Frame(self.window)
        self.mainframe.pack()

        # frame and frame2 packed into main frame
        self.frame = Frame(self.mainframe, padx=15, pady=15)
        self.frame.pack(fill=X)

        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        # Shows dates tool has been booked:

        # Label for selected tool
        self.bkgs_lbl = Label(self.frame, text=("Tool ID " + str(self.slcted_tl) + " Booked on Following Dates:"))
        self.bkgs_lbl.pack()

        # Create Scrollbar
        self.bkgs_scrlbar = Scrollbar(self.frame, orient=VERTICAL)

        # Create Bookings Listbox
        self.bkgs_lstbx = Listbox(self.frame, width=50, yscrollcommand=self.bkgs_scrlbar)

        # Configure Scrollbar
        self.bkgs_scrlbar.config(command=self.bkgs_lstbx.yview)
        self.bkgs_scrlbar.pack(side=RIGHT, fill=Y)

        # Pack the Listbox with Scrollbar
        self.bkgs_lstbx.pack()

        # Call all bookings and add them to the Listbox
        self.tl_bkgs = SQLRead().get_bookings_by_tid(self.slcted_tl)
        for x in self.tl_bkgs:
            self.bkg_id = x[0]
            self.st_time = x[3]
            self.end_time = x[4]
            self.tl_bkgs_short = "#{}#  {}  to  {}".format(str(self.bkg_id), str(self.st_time), str(self.end_time))
            self.bkgs_lstbx.insert(END, self.tl_bkgs_short)

        # Make Booking:

        self.mk_bkg_lbl = Label(self.frame2, text="Make a Booking")
        self.mk_bkg_lbl.pack()

        self.start_date_lbl = Label(self.frame2, text="Start Date of Booking")
        self.start_date_lbl.pack()

        # Load Calendar for start date from tkcalendar import
        self.start_cal = Calendar(self.frame2)
        self.start_cal.pack()

        self.end_date_lbl = Label(self.frame2, text="End Date of Booking")
        self.end_date_lbl.pack()

        # Load Calendar for end date  from tkcalendar import
        self.end_cal = Calendar(self.frame2)
        self.end_cal.pack()

        self.end_date_lbl = Label(self.frame2, text="Please select if this is required all day,\n "
                                                    "in the morning only (AM) or in the afternoon only (PM). \n"
                                                    "Bookings made over multiple days will be charged a full \n"
                                                    "day regardless of the option selected. Tools may only be \n"
                                                    "booked for 3 days at a time.")
        self.end_date_lbl.pack()

        # Radio Buttons for time of booking
        modes = [
            ("ALL DAY", "ALL DAY"),
            ("AM", "AM"),
            ("PM", "PM"),
        ]

        self.time_rb_var = StringVar()
        self.time_rb_var.set("ALL DAY")
        for text, mode in modes:
            Radiobutton(self.frame2, text=text, variable=self.time_rb_var, value=mode).pack()

        self.deliv_collect_lbl = Label(self.frame2, text="Delivery or Collection?")
        self.deliv_collect_lbl.pack()

        # Radio Buttons for Delivery or Collection
        self.dc_rb_var = StringVar()
        self.dc_rb_var.set("Delivery")

        Radiobutton(self.frame2, text="Delivery", variable=self.dc_rb_var, value="Delivery").pack()
        Radiobutton(self.frame2, text="Collection", variable=self.dc_rb_var, value="Collection").pack()

        # Submit Booking button call calls the make_booking function
        self.mk_bkg_btn = Button(self.frame2, text="Submit Booking", command=self.make_booking)
        self.mk_bkg_btn.pack()

    def make_booking(self):
        """Retrieves values of user's selections and checks if they are valid.
        If valid, the booking will be inserted into the bookings table in the DB."""
        # Retrieves values selected for calendars
        start_date = self.start_cal.get_date()
        end_date = self.end_cal.get_date()

        # Retrieves radio button
        time = self.time_rb_var.get()

        # Format to required to input into DB
        start_time = str(start_date) + ':' + time
        end_time = str(end_date) + ':' + time

        # Retrieves radio button
        deliv_collect = self.dc_rb_var.get()

        # Calculations required for invalid inputs:

        # Uses datetime import to calculate days between two dates
        first_date = date((int(start_date.split('/')[2]) + 2000),
                          int(start_date.split('/')[0]),
                          int(start_date.split('/')[1]))
        second_date = date((int(end_date.split('/')[2]) + 2000),
                           int(end_date.split('/')[0]),
                           int(end_date.split('/')[1]))
        today = date.today()  # Today's date
        date_length = (second_date - first_date).days
        date_length2 = (first_date - today).days

        # the boolean value err will be changed to true if the requested time is invalid
        # Uses for loop to do check against each booking on a particular tool

        err = False
        if date_length > 2 or date_length2 < 0:
            err = True

        for x in self.tl_bkgs:
            x_start_date = x[3].split(':')[0]
            x_start_date_dt = date((int(x_start_date.split('/')[2]) + 2000),
                                 int(x_start_date.split('/')[0]),
                                 int(x_start_date.split('/')[1]))
            x_end_date = x[4].split(':')[0]
            x_end_date_dt = date((int(x_end_date.split('/')[2]) + 2000),
                                 int(x_end_date.split('/')[0]),
                                 int(x_end_date.split('/')[1]))
            date_length3 = (x_end_date_dt - x_start_date_dt).days

            if date_length3 == 2:
                start_date_mod = date((int(start_date.split('/')[2]) + 2000),
                                    int(start_date.split('/')[0]),
                                    int(start_date.split('/')[1])) + datetime.timedelta(days=1)
                end_date_mod = date((int(end_date.split('/')[2]) + 2000),
                                      int(end_date.split('/')[0]),
                                      int(end_date.split('/')[1])) - datetime.timedelta(days=1)
                if (end_date_mod == x_start_date_dt) or (start_date_mod == x_end_date_dt):
                    err = True
            if start_time == x[3]:
                err = True
            if start_time == x[4]:
                err = True
            if start_date == x[3].split(':')[0]:
                if x[3].split(':')[1] == "ALL DAY":
                    err = True
                if (x[3].split(':')[1] == "AM") and (time == "AM"):
                    err = True
                if (x[3].split(':')[1] == "PM") and (time == "PM"):
                    err = True
                if ((x[3].split(':')[1] == "AM") or (x[3].split(':')[1] == "PM")) and (time == "ALL DAY"):
                    err = True


        # Error label appears for invalid input
        if err:
            date_err_lbl = Label(self.frame2, text="You cannot make this booking.", fg='red')
            date_err_lbl.pack()
        # Valid input inserts booking into DB by calling the relevant function from the SQLCreate class
        else:
            # Uses Booking class to temporarily store captured data.
            bkg = Booking(booking_id='', tool_id=self.slcted_tl, booked_by=self.uid_token,
                          start_time=start_time, end_time=end_time, deliv_collect=deliv_collect,
                          courier_id='', completed='No', days_late=0)
            # Instance of booking inserted into table of DB
            SQLCreate().insert_booking(bkg)
            # Window is destroyed when booking is made
            self.window.destroy()


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    BookTool(root, 'tu1', 1)
    root.mainloop()
