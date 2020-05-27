from tkinter import *
from tkcalendar import *
from PIL import ImageTk, Image
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from datetime import date
import Shared_Power.DB.sql_read as sqlr

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()

today = date.today()

class MyInvoices:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.window = Toplevel()

        self.window.title("My Invoices")

        self.frame = Frame(self.window)
        self.frame.pack()

        self.frame2 = Frame(self.window)
        self.frame2.pack()

        # Call the user from the DB and check their user type
        self.this_usr = sqlr.get_user_by_id(self.uid_token)
        self.usr_type = self.this_usr[0][2]

        self.month_lbl = Label(self.frame, text="Select Month")
        self.month_lbl.pack()
        self.month_var = IntVar()
        self.month_var.set(1)
        self.month_opt = OptionMenu(self.frame, self.month_var, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.month_opt.pack()

        self.year_lbl = Label(self.frame, text="Select Year")
        self.year_lbl.pack()
        self.year_var = IntVar()
        self.year_var.set(20)
        self.year_opt = OptionMenu(self.frame, self.year_var, 20, 21, 22)
        self.year_opt.pack()

        self.slct_btn = Button(self.frame, text="Select", command=self.select)
        self.slct_btn.pack()

    def select(self):
        self.frame2.destroy()

        self.frame2 = Frame(self.window)
        self.frame2.pack()

        month = self.month_var.get()
        year = self.year_var.get()

        # Call the user's or tool's bookings depending on user type
        if self.usr_type == "Tool Owner":
            self.inv_tl_own(month, year)
        if self.usr_type == "Tool User":
            self.inv_tl_usr(month, year)
        if self.usr_type == "Dispatch Rider":
            self.inv_dptch_rdr(month, year)

    def inv_tl_own(self, month, year):
        first_date = date((year+2000), (month+1), 1)
        second_date = today
        date_length = (second_date - first_date).days
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        else:
            my_tls = sqlr.get_tools_by_uid(self.uid_token)
            my_tls_ids = []
            for x in my_tls:
                if x[0] != []:
                    my_tls_ids.append(x[0])

            my_bkgs = []
            for x in my_tls_ids:
                a_bkg = sqlr.get_bookings_by_tid(x)
                if a_bkg != []:
                    my_bkgs.append(a_bkg)

            bkg_totals = 0
            late_fee_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                this_tl = sqlr.get_tool_by_id(x[0][1])

                start_time = x[0][3]
                end_time = x[0][4]

                start_date = start_time.split(':')[0]
                end_date = end_time.split(':')[0]
                day_time = start_time.split(':')[1]
                #print(start_date, end_date, day_time)

                if int(end_date.split('/')[0]) == month:
                    start_date_dt = date(int(start_date.split('/')[2]), int(start_date.split('/')[0]),
                                      int(start_date.split('/')[1]))
                    end_date_dt = date(int(end_date.split('/')[2]), int(end_date.split('/')[0]), int(end_date.split('/')[1]))

                    date_length = (end_date_dt - start_date_dt).days

                    if date_length == 0:
                        if day_time == "ALL DAY":
                            price = this_tl[0][4]
                        else:
                            price = this_tl[0][5]
                    else:
                        price = this_tl[0][4] * (date_length + 1)

                    show_bkg_price = "£{:,.2f}".format(price)
                    bkg_price_lbl = Label(self.frame2, text=("Booking ID " + str(x[0][0]) + " price: " + show_bkg_price))
                    bkg_price_lbl.pack()

                    late_fee = price * x[0][8]
                    show_late_fee = "£{:,.2f}".format(late_fee)
                    late_fee_lbl = Label(self.frame2, text=("Booking ID " + str(x[0][0]) + " late fee: " + show_late_fee))
                    late_fee_lbl.pack()

                    bkg_totals += price
                    late_fee_totals += late_fee

                    if x[0][7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0][0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()

            show_bkg_totals = "£{:,.2f}".format(bkg_totals)
            bkg_totals_lbl = Label(self.frame2, text=("Total income from bookings: " + show_bkg_totals))
            bkg_totals_lbl.pack()

            show_late_fee_totals = "£{:,.2f}".format(late_fee_totals)
            late_fee_totals_lbl = Label(self.frame2, text=("Total income from late fees: " + show_late_fee_totals))
            late_fee_totals_lbl.pack()

            if bkg_totals == 0:
                insure_charge = 0
            else:
                insure_charge = 5

            show_insure_charge = "£{:,.2f}".format(insure_charge)
            ins_chrg_lbl = Label(self.frame2, text=("Insurance charge: " + show_insure_charge))
            ins_chrg_lbl.pack()

            if open_bkgs == True:
                open_bkgs_lbl = Label(self.frame2,
                                      text="You still have open booking, therefore this invoice is still open.",
                                      fg='blue')
                open_bkgs_lbl.pack()
            else:
                open_bkgs_lbl = Label(self.frame2, text="This invoice is closed.", fg='green')
                open_bkgs_lbl.pack()

    def inv_tl_usr(self, month, year):
        first_date = date((year+2000), (month+1), 1)
        second_date = today
        date_length = (second_date - first_date).days
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        else:
            my_bkgs = sqlr.get_bookings_by_booker(self.uid_token)

            bkg_totals = 0
            deliv_chrg_totals = 0
            late_fee_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                this_tl = sqlr.get_tool_by_id(x[1])

                start_time = x[3]
                end_time = x[4]

                start_date = start_time.split(':')[0]
                end_date = end_time.split(':')[0]
                day_time = start_time.split(':')[1]
                #print(start_date, end_date, day_time)

                if int(end_date.split('/')[0]) == month:
                    start_date_dt = date(int(start_date.split('/')[2]), int(start_date.split('/')[0]),
                                      int(start_date.split('/')[1]))
                    end_date_dt = date(int(end_date.split('/')[2]), int(end_date.split('/')[0]), int(end_date.split('/')[1]))

                    date_length = (end_date_dt - start_date_dt).days

                    if date_length == 0:
                        if day_time == "ALL DAY":
                            price = this_tl[0][4]
                        else:
                            price = this_tl[0][5]
                    else:
                        price = this_tl[0][4] * (date_length + 1)

                    show_bkg_price = "£{:,.2f}".format(price)
                    bkg_price_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) + " price: " + show_bkg_price))
                    bkg_price_lbl.pack()

                    if x[5] == "Delivery":
                        deliv_charge = 4
                        show_deliv_chrg = "£{:,.2f}".format(deliv_charge)
                        deliv_chrg_lbl = Label(self.frame2,
                                               text=("Booking ID " + str(x[0]) +
                                                     " delivery charge: " + show_deliv_chrg))
                        deliv_chrg_lbl.pack()
                    else:
                        deliv_charge = 0

                    late_fee = price * x[8]
                    show_late_fee = "£{:,.2f}".format(late_fee)
                    late_fee_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) + " late fee: " + show_late_fee))
                    late_fee_lbl.pack()

                    bkg_totals += price
                    deliv_chrg_totals += deliv_charge
                    late_fee_totals += late_fee

                    if x[7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()

            show_bkg_totals = "£{:,.2f}".format(bkg_totals)
            bkg_totals_lbl = Label(self.frame2, text=("Total cost of bookings: " + show_bkg_totals))
            bkg_totals_lbl.pack()

            show_deliv_chrg_totals = "£{:,.2f}".format(deliv_chrg_totals)
            deliv_chrg_totals_lbl = Label(self.frame2, text=("Total cost of delivery charges: " + show_deliv_chrg_totals))
            deliv_chrg_totals_lbl.pack()

            show_late_fee_totals = "£{:,.2f}".format(late_fee_totals)
            late_fee_totals_lbl = Label(self.frame2, text=("Total cost of late fees: " + show_late_fee_totals))
            late_fee_totals_lbl.pack()

            if bkg_totals == 0:
                insure_charge = 0
            else:
                insure_charge = 5

            show_insure_charge = "£{:,.2f}".format(insure_charge)
            ins_chrg_lbl = Label(self.frame2, text=("Insurance charge: " + show_insure_charge))
            ins_chrg_lbl.pack()

            if open_bkgs == True:
                open_bkgs_lbl = Label(self.frame2,
                                      text="You still have open booking, therefore this invoice is still open.",
                                      fg='blue')
                open_bkgs_lbl.pack()
            else:
                open_bkgs_lbl = Label(self.frame2, text="This invoice is closed.", fg='green')
                open_bkgs_lbl.pack()

    def inv_dptch_rdr(self, month, year):
        first_date = date((year+2000), (month+1), 1)
        second_date = today
        date_length = (second_date - first_date).days
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        else:
            my_bkgs = sqlr.get_bookings_by_courier(self.uid_token)

            deliv_chrg_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                end_time = x[4]
                end_date = end_time.split(':')[0]

                if int(end_date.split('/')[0]) == month:

                    if x[5] == "Delivery":
                        deliv_charge = 4
                        show_deliv_chrg = "£{:,.2f}".format(deliv_charge)
                        deliv_chrg_lbl = Label(self.frame2,
                                               text=("Booking ID " + str(x[0]) +
                                                     " delivery charge: " + show_deliv_chrg))
                        deliv_chrg_lbl.pack()
                    else:
                        deliv_charge = 0

                    deliv_chrg_totals += deliv_charge

                    if x[7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()

            show_deliv_chrg_totals = "£{:,.2f}".format(deliv_chrg_totals)
            deliv_chrg_totals_lbl = Label(self.frame2, text=("Total delivery earnings: " + show_deliv_chrg_totals))
            deliv_chrg_totals_lbl.pack()

            if deliv_chrg_totals == 0:
                insure_charge = 0
            else:
                insure_charge = 5

            show_insure_charge = "£{:,.2f}".format(insure_charge)
            ins_chrg_lbl = Label(self.frame2, text=("Insurance charge: " + show_insure_charge))
            ins_chrg_lbl.pack()

            if open_bkgs == True:
                open_bkgs_lbl = Label(self.frame2,
                                      text="You still have open booking, therefore this invoice is still open.",
                                      fg='blue')
                open_bkgs_lbl.pack()
            else:
                open_bkgs_lbl = Label(self.frame2, text="This invoice is closed.", fg='green')
                open_bkgs_lbl.pack()





if __name__ == "__main__":
    root = Tk()
    MyInvoices(root, 'rider1')
    root.mainloop()