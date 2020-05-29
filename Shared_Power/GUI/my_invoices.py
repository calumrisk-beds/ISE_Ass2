from tkinter import *
import shutil
import datetime
from datetime import date
from dateutil.relativedelta import *
from Shared_Power.DB.sql_read import SQLRead


class MyInvoices:
    """The user's invoice, designed to show the relevant details per user.
            Tk() is passed into master from previous class, allowing main Tkinter window to run.
            The user's ID is passed into uid_token."""

    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        # New window
        self.window = Toplevel()

        # Window title
        self.window.title("My Invoices")

        # Main frame packed into window
        self.mainframe = Frame(self.window)
        self.mainframe.pack()

        # Frame packed into main frame
        self.frame = Frame(self.mainframe)
        self.frame.pack()

        # Frame 2 packed into main frame
        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        # Today defined with datetime import
        self.today = date.today()

        # Call the user from the DB and check their user type
        self.this_usr = SQLRead().get_user_by_id(self.uid_token)
        self.usr_type = self.this_usr[0][2]

        # Option Menu for user to select invoice month
        self.month_lbl = Label(self.frame, text="Select Month")
        self.month_lbl.pack()
        self.month_var = IntVar()
        self.month_var.set(1)
        self.month_opt = OptionMenu(self.frame, self.month_var, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.month_opt.pack()

        # Option Menu for user to select invoice year
        self.year_lbl = Label(self.frame, text="Select Year")
        self.year_lbl.pack()
        self.year_var = IntVar()
        self.year_var.set(20)
        self.year_opt = OptionMenu(self.frame, self.year_var, 20, 21, 22)
        self.year_opt.pack()

        # Show Invoice button
        self.show_inv_btn = Button(self.frame, text="Show Invoice", command=self.show_inv)
        self.show_inv_btn.pack()

    def show_inv(self):
        """Called when show invoice button is selected."""
        # Destroys Frame 2
        # This is useful when the user switches the invoice they are viewing because it will clear the previous invoice
        self.frame2.destroy()

        # Re create Frame 2 ready for the next invoice
        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        # Retrieves selected options
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
        """Called for Tool Owner when the show invoices button is selected.
            month and year passed into method."""
        # Calculations to determine if a future invoice is trying to be fetched
        # +2000 to match datetime year and +1 for month because invoices are generated at the end of every month
        first_date = date((year+2000), month, 1) + relativedelta(months=+1)
        second_date = self.today
        date_length = (second_date - first_date).days
        # Error label is displayed if future invoice is attempted to be fetched
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        # Proceeds with code to determine other invoice parameters if there is not an error
        else:
            # Retrieves Tool Owner's tools from tools table in DB by calling the relevant function from sqr
            my_tls = SQLRead().get_tools_by_uid(self.uid_token)

            # List defined that will store Tool Owner's Tool IDs
            my_tls_ids = []
            # For Loop to check each tool fetched from tools table
            for x in my_tls:
                # Appends my_tls_ids list with each Tool ID, only if this is not blank
                if x[0] != []:
                    my_tls_ids.append(x[0])
            # List defined that will store the Tool Owner's Bookings
            my_bkgs = []
            # For Loop to check each of the Tool Owner's Tool IDs that have now been defined
            for x in my_tls_ids:
                # Fetches
                tl_bkgs = SQLRead().get_bookings_by_tid(x)
                for y in tl_bkgs:
                    if y != []:
                        my_bkgs.append(y)

            bkg_totals = 0
            late_fee_totals = 0
            dmg_charge_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                this_tl = SQLRead().get_tool_by_id(x[1])


                start_time = x[3]
                end_time = x[4]

                start_date = start_time.split(':')[0]
                end_date = end_time.split(':')[0]
                day_time = start_time.split(':')[1]

                if (int(end_date.split('/')[0]) == month) and (int(end_date.split('/')[2]) == year):
                    cases = SQLRead().get_cases_by_bid(x[0])
                    bkg_damage_chrg = 0
                    for y in cases:
                        if y[8] == self.uid_token:
                            this_charge = y[9]
                            bkg_damage_chrg += this_charge

                    start_date_dt = date(int(start_date.split('/')[2]), int(start_date.split('/')[0]),
                                      int(start_date.split('/')[1]))
                    end_date_dt = date(int(end_date.split('/')[2]), int(end_date.split('/')[0]),
                                       int(end_date.split('/')[1]))

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

                    late_fee = price * x[8]
                    show_late_fee = "£{:,.2f}".format(late_fee)
                    late_fee_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) + " late fee: " + show_late_fee))
                    late_fee_lbl.pack()

                    show_bkg_dmg_chrg = "£{:,.2f}".format(bkg_damage_chrg)
                    bkg_dmg_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) +
                                                           " your damage charges: " + show_bkg_dmg_chrg))
                    bkg_dmg_lbl.pack()



                    bkg_totals += price
                    late_fee_totals += late_fee
                    dmg_charge_totals += bkg_damage_chrg

                    if x[7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()

            inv_divider_lbl = Label(self.frame2, text="---------------------------------")
            inv_divider_lbl.pack()

            show_bkg_totals = "£{:,.2f}".format(bkg_totals)
            bkg_totals_lbl = Label(self.frame2, text=("Total income from bookings: " + show_bkg_totals), fg='green')
            bkg_totals_lbl.pack()

            show_late_fee_totals = "£{:,.2f}".format(late_fee_totals)
            late_fee_totals_lbl = Label(self.frame2, text=("Total income from late fees: " + show_late_fee_totals),
                                        fg='green')
            late_fee_totals_lbl.pack()

            show_dmg_chrg_totals = "£{:,.2f}".format(dmg_charge_totals)
            dmg_chrg_totals_lbl = Label(self.frame2, text=("Total damage charges: " + show_dmg_chrg_totals), fg='red')
            dmg_chrg_totals_lbl.pack()

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
        # Calculations to determine if a future invoice is trying to be fetched
        # +2000 to match datetime year and +1 for month because invoices are generated at the end of every month
        first_date = date((year + 2000), month, 1) + relativedelta(months=+1)
        second_date = self.today
        date_length = (second_date - first_date).days
        # Error label is displayed if future invoice is attempted to be fetched
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        # Proceeds with code to determine other invoice parameters if there is not an error
        else:
            my_bkgs = SQLRead().get_bookings_by_booker(self.uid_token)

            bkg_totals = 0
            deliv_chrg_totals = 0
            late_fee_totals = 0
            dmg_charge_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                this_tl = SQLRead().get_tool_by_id(x[1])

                start_time = x[3]
                end_time = x[4]

                start_date = start_time.split(':')[0]
                end_date = end_time.split(':')[0]
                day_time = start_time.split(':')[1]
                #print(start_date, end_date, day_time)

                if (int(end_date.split('/')[0]) == month) and (int(end_date.split('/')[2]) == year):
                    cases = SQLRead().get_cases_by_bid(x[0])
                    bkg_damage_chrg = 0
                    for y in cases:
                        if y[8] == self.uid_token:
                            this_charge = y[9]
                            bkg_damage_chrg += this_charge

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

                    show_bkg_dmg_chrg = "£{:,.2f}".format(bkg_damage_chrg)
                    bkg_dmg_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) +
                                                           " your damage charges: " + show_bkg_dmg_chrg))
                    bkg_dmg_lbl.pack()

                    bkg_totals += price
                    deliv_chrg_totals += deliv_charge
                    late_fee_totals += late_fee
                    dmg_charge_totals += bkg_damage_chrg

                    if x[7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()

            inv_divider_lbl = Label(self.frame2, text="---------------------------------")
            inv_divider_lbl.pack()

            show_bkg_totals = "£{:,.2f}".format(bkg_totals)
            bkg_totals_lbl = Label(self.frame2, text=("Total cost of bookings: " + show_bkg_totals))
            bkg_totals_lbl.pack()

            show_deliv_chrg_totals = "£{:,.2f}".format(deliv_chrg_totals)
            deliv_chrg_totals_lbl = Label(self.frame2, text=("Total cost of delivery charges: " + show_deliv_chrg_totals))
            deliv_chrg_totals_lbl.pack()

            show_dmg_chrg_totals = "£{:,.2f}".format(dmg_charge_totals)
            dmg_chrg_totals_lbl = Label(self.frame2, text=("Total damage charges: " + show_dmg_chrg_totals), fg='red')
            dmg_chrg_totals_lbl.pack()

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
        # Calculations to determine if a future invoice is trying to be fetched
        # +2000 to match datetime year and +1 for month because invoices are generated at the end of every month
        first_date = date((year + 2000), month, 1) + relativedelta(months=+1)
        second_date = self.today
        date_length = (second_date - first_date).days
        # Error label is displayed if future invoice is attempted to be fetched
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        # Proceeds with code to determine other invoice parameters if there is not an error
        else:
            my_bkgs = SQLRead().get_bookings_by_courier(self.uid_token)

            deliv_chrg_totals = 0
            dmg_charge_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                end_time = x[4]
                end_date = end_time.split(':')[0]

                if (int(end_date.split('/')[0]) == month) and (int(end_date.split('/')[2]) == year):
                    cases = SQLRead().get_cases_by_bid(x[0])
                    bkg_damage_chrg = 0
                    for y in cases:
                        if y[8] == self.uid_token:
                            this_charge = y[9]
                            bkg_damage_chrg += this_charge

                    if x[5] == "Delivery":
                        deliv_charge = 4
                        show_deliv_chrg = "£{:,.2f}".format(deliv_charge)
                        deliv_chrg_lbl = Label(self.frame2,
                                               text=("Booking ID " + str(x[0]) +
                                                     " delivery charge: " + show_deliv_chrg))
                        deliv_chrg_lbl.pack()
                    else:
                        deliv_charge = 0

                        show_bkg_dmg_chrg = "£{:,.2f}".format(bkg_damage_chrg)
                        bkg_dmg_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) +
                                                               " your damage charges: " + show_bkg_dmg_chrg))
                        bkg_dmg_lbl.pack()

                    deliv_chrg_totals += deliv_charge
                    dmg_charge_totals += bkg_damage_chrg

                    if x[7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()


            show_deliv_chrg_totals = "£{:,.2f}".format(deliv_chrg_totals)
            deliv_chrg_totals_lbl = Label(self.frame2, text=("Total delivery earnings: " + show_deliv_chrg_totals))
            deliv_chrg_totals_lbl.pack()

            show_dmg_chrg_totals = "£{:,.2f}".format(dmg_charge_totals)
            dmg_chrg_totals_lbl = Label(self.frame2, text=("Total damage charges: " + show_dmg_chrg_totals), fg='red')
            dmg_chrg_totals_lbl.pack()

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


    def inv_dptch_rdr(self, month, year):
        # Calculations to determine if a future invoice is trying to be fetched
        # +2000 to match datetime year and +1 for month because invoices are generated at the end of every month
        first_date = date((year + 2000), month, 1) + relativedelta(months=+1)
        second_date = self.today
        date_length = (second_date - first_date).days
        # Error label is displayed if future invoice is attempted to be fetched
        if date_length < 0:
            date_err_lbl = Label(self.frame2, text="You can only select past invoices", fg='red')
            date_err_lbl.pack()
        # Proceeds with code to determine other invoice parameters if there is not an error
        else:
            my_bkgs = SQLRead().get_bookings_by_courier(self.uid_token)

            deliv_chrg_totals = 0
            dmg_charge_totals = 0
            open_bkgs = False
            for x in my_bkgs:
                end_time = x[4]
                end_date = end_time.split(':')[0]

                if (int(end_date.split('/')[0]) == month) and (int(end_date.split('/')[2]) == year):
                    cases = SQLRead().get_cases_by_bid(x[0])
                    bkg_damage_chrg = 0
                    for y in cases:
                        if y[8] == self.uid_token:
                            this_charge = y[9]
                            bkg_damage_chrg += this_charge

                    if x[5] == "Delivery":
                        deliv_charge = 4
                        show_deliv_chrg = "£{:,.2f}".format(deliv_charge)
                        deliv_chrg_lbl = Label(self.frame2,
                                               text=("Booking ID " + str(x[0]) +
                                                     " delivery charge: " + show_deliv_chrg))
                        deliv_chrg_lbl.pack()
                    else:
                        deliv_charge = 0

                        show_bkg_dmg_chrg = "£{:,.2f}".format(bkg_damage_chrg)
                        bkg_dmg_lbl = Label(self.frame2, text=("Booking ID " + str(x[0]) +
                                                               " your damage charges: " + show_bkg_dmg_chrg))
                        bkg_dmg_lbl.pack()

                    deliv_chrg_totals += deliv_charge
                    dmg_charge_totals += bkg_damage_chrg

                    if x[7] == "No":
                        open_bkgs = True
                        open_bkg_lbl = Label(self.frame2,
                                             text=("Booking ID " + str(x[0]) + " is still open"),
                                             fg='red')
                        open_bkg_lbl.pack()


            show_deliv_chrg_totals = "£{:,.2f}".format(deliv_chrg_totals)
            deliv_chrg_totals_lbl = Label(self.frame2, text=("Total delivery earnings: " + show_deliv_chrg_totals))
            deliv_chrg_totals_lbl.pack()

            show_dmg_chrg_totals = "£{:,.2f}".format(dmg_charge_totals)
            dmg_chrg_totals_lbl = Label(self.frame2, text=("Total damage charges: " + show_dmg_chrg_totals), fg='red')
            dmg_chrg_totals_lbl.pack()

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
    MyInvoices(root, 'dr1')
    root.mainloop()