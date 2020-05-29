from tkinter import *
from Shared_Power.GUI.view_tools import ViewTools
from Shared_Power.GUI.my_bookings import MyBookings
from Shared_Power.GUI.my_invoices import MyInvoices


class ToolUserView:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Tool User")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.vw_tl_btn = Button(self.frame, text="Book Tool", command=self.vw_tools)
        self.vw_tl_btn.pack()

        self.mng_bkgs_btn = Button(self.frame, text="Manage Bookings", command=self.mng_bookings)
        self.mng_bkgs_btn.pack()

        self.my_inv_btn = Button(self.frame, text="My Invoices", command=self.my_inv)
        self.my_inv_btn.pack()

    def vw_tools(self):
        # Call ViewTolls
        ViewTools(self.master, self.uid_token)

    def mng_bookings(self):
        # Call MyBookings
        MyBookings(self.master, self.uid_token, '')

    def my_inv(self):
        MyInvoices(self.master, self.uid_token)


if __name__ == "__main__":
    root = Tk()
    ToolUserView(root, 'test5')
    root.mainloop()
