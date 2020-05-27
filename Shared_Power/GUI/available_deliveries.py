from tkinter import *
from tkcalendar import *
from PIL import ImageTk, Image
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from Shared_Power.GUI.manage_booking import ManageBooking
import Shared_Power.DB.sql_read as sqlr

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()


class AvailableDeliveries:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.window = Toplevel()

        self.window.title("Available Deliveries")

        self.frame = Frame(self.window, padx=15, pady=15)
        self.frame.pack(fill=X)

        self.open_bkgs_lbl = Label(self.frame, text="Open Bookings")
        self.open_bkgs_lbl.pack()

        # Create Scrollbar
        self.bkgs_scrlbar = Scrollbar(self.frame, orient=VERTICAL)

        # Create Bookings Listbox
        self.bkgs_lstbx = Listbox(self.frame, width=50, yscrollcommand=self.bkgs_scrlbar)

        # Configure Scrollbar
        self.bkgs_scrlbar.config(command=self.bkgs_lstbx.yview)
        self.bkgs_scrlbar.pack(side=RIGHT, fill=Y)

        # Pack the Listbox with Scrollbar
        self.bkgs_lstbx.pack(fill=X)

        # Call available deliveries from DB
        self.avai_delivs = sqlr.get_available_bookings_by_delivery()

        for x in self.avai_delivs:
            self.bkg_id = x[0]
            self.bkg_tl = x[1]
            self.bkg_start = x[3]
            self.bkg_end = x[4]
            self.bkg_dc = x[5]
            self.bkgs_short = "#{}#  Tool ID: {}  {}  to  {}  ({})".format(str(self.bkg_id), str(self.bkg_tl),
                                                                           str(self.bkg_start), str(self.bkg_end),
                                                                           str(self.bkg_dc))
            self.bkgs_lstbx.insert(END, self.bkgs_short)

            # Select Booking Button
            self.slct_bkg_btn = Button(self.frame, text="Select", command=self.select_bkg)
            self.slct_bkg_btn.pack()

    def select_bkg(self):
        # Retrieves selected item and splits the string to retrieve the Booking ID
        selected = self.bkgs_lstbx.get(ANCHOR)
        selected_bid = selected.split('#')[1]

        # Destroy window
        self.window.destroy()

        # Call ManageBooking and pass the value of User ID and Booking ID
        ManageBooking(self.master, self.uid_token, selected_bid)
