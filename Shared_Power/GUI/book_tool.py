from tkinter import *
from tkcalendar import *
from PIL import ImageTk, Image
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.GUI.my_tools import MyTools
from Shared_Power.GUI.manage_tool import ManageTool
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool
from Shared_Power.Classes.booking import Booking

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()


class BookTool:
    def __init__(self, master, uid_token, slcted_tl):
        self.master = master
        self.uid_token = uid_token
        self.slcted_tl = slcted_tl

        self.master.title("Book Tool")

        self.mainframe = Frame(self.master)
        self.mainframe.pack()

        self.frame = Frame(self.mainframe, padx=15, pady=15)
        self.frame.pack(fill=X)

        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        # Shows dates tool has been booked
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
        self.tl_bkgs = sqlr.get_bookings_by_tid(self.slcted_tl)
        for x in self.tl_bkgs:
            self.bkg_id = x[0]
            self.st_time = x[3]
            self.end_time = x[3]
            self.tl_bkgs_short = "#{}#  {}  to  {}".format(str(self.bkg_id), str(self.st_time), str(self.end_time))
            self.bkgs_lstbx.insert(END, self.tl_bkgs_short)

        # Make Booking
        self.mk_bkg_lbl = Label(self.frame2, text="Make a Booking")
        self.mk_bkg_lbl.pack()

        self.start_date_lbl = Label(self.frame2, text="Start Date of Booking")
        self.start_date_lbl.pack()

        # Load Calendar for start date
        self.start_cal = Calendar(self.frame2)
        self.start_cal.pack()

        self.end_date_lbl = Label(self.frame2, text="End Date of Booking")
        self.end_date_lbl.pack()

        # Load Calendar for end date
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

        self.mk_bkg_btn = Button(self.frame2, text="Submit Booking", command=self.make_booking)
        self.mk_bkg_btn.pack()

    def make_booking(self):
        start_date = self.start_cal.get_date()
        end_date = self.end_cal.get_date()
        time = self.time_rb_var.get()

        start_time = str(start_date) + ':' + time
        end_time = str(end_date) + ':' + time

        deliv_collect = self.dc_rb_var.get()
        print(deliv_collect)

        bkg = Booking(booking_id='', tool_id=self.slcted_tl, booked_by=self.uid_token,
                      start_time=start_time, end_time=end_time, deliv_collect=deliv_collect, completed='No')

        sqlc.insert_booking(bkg)


if __name__ == "__main__":
    root = Tk()
    BookTool(root, 'test5', 4)
    root.mainloop()