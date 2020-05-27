from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from Shared_Power.GUI.my_bookings import MyBookings
from Shared_Power.GUI.available_deliveries import AvailableDeliveries
from Shared_Power.GUI.my_invoices import MyInvoices

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()


class DispatchRiderView:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Dispatch Rider")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.avai_delivs_btn = Button(self.frame, text="Available Deliveries", command=self.available_delivs)
        self.avai_delivs_btn.pack()

        self.my_delivs_btn = Button(self.frame, text="My Deliveries", command=self.my_delivs)
        self.my_delivs_btn.pack()

        self.my_inv_btn = Button(self.frame, text="My Invoices", command=self.my_inv)
        self.my_inv_btn.pack()

    def available_delivs(self):
        AvailableDeliveries(self.master, self.uid_token)

    def my_delivs(self):
        MyBookings(self.master, self.uid_token, '')

    def my_inv(self):
        MyInvoices(self.master, self.uid_token)