from tkinter import *
from Shared_Power.GUI.add_condition import AddCondition
from Shared_Power.DB.sql_read import SQLRead
from Shared_Power.DB.sql_update import SQLUpdate
from Shared_Power.DB.sql_delete import SQLDelete


class ManageBooking:
    def __init__(self, master, uid_token, slcted_bkg):
        self.master = master
        self.uid_token = uid_token
        self.slcted_bkg = slcted_bkg

        self.window = Toplevel()

        self.window.title("Manage Booking")

        self.mainframe = Frame(self.window)
        self.mainframe.pack()

        self.frame = Frame(self.mainframe)
        self.frame.pack()

        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        # Fetch details from DB
        self.this_usr = SQLRead().get_user_by_id(self.uid_token)
        self.this_bkg = SQLRead().get_booking_by_id(self.slcted_bkg)
        self.this_tl = SQLRead().get_tool_by_id(self.this_bkg[0][1])
        self.tl_owner_usr = SQLRead().get_user_by_id(self.this_tl[0][1])
        self.bked_by = SQLRead().get_user_by_id(self.this_bkg[0][2])
        self.cour_usr = SQLRead().get_user_by_id(self.this_bkg[0][6])
        self.cases = SQLRead().get_cases_by_bid(self.slcted_bkg)

        # Display Booking and Tool Details
        self.bkg_details_lbl = Label(self.frame, text="Booking Details")
        self.bkg_details_lbl.grid(column=0, row=0, padx=20)

        self.bkg_id_lbl = Label(self.frame, text="Booking ID:")
        self.bkg_id_lbl.grid(column=0, row=1)
        self.this_bkg_id = Label(self.frame, text=self.this_bkg[0][0])
        self.this_bkg_id.grid(column=1, row=1)

        self.tl_name_lbl = Label(self.frame, text="Tool Name:")
        self.tl_name_lbl.grid(column=0, row=2)
        self.this_tl_name = Label(self.frame, text=self.this_tl[0][2])
        self.this_tl_name.grid(column=1, row=2)

        self.tl_descr_lbl = Label(self.frame, text="Tool Description:")
        self.tl_descr_lbl.grid(column=0, row=3)
        self.this_tl_descr = Label(self.frame, text=self.this_tl[0][3])
        self.this_tl_descr.grid(column=1, row=3)

        self.start_time_lbl = Label(self.frame, text="Booking Start Time:")
        self.start_time_lbl.grid(column=0, row=4)
        self.this_bkg_st = Label(self.frame, text=self.this_bkg[0][3])
        self.this_bkg_st.grid(column=1, row=4)

        self.end_time_lbl = Label(self.frame, text="Booking End Time:")
        self.end_time_lbl.grid(column=0, row=5)
        self.this_bkg_et = Label(self.frame, text=self.this_bkg[0][4])
        self.this_bkg_et.grid(column=1, row=5)

        self.deliv_collect_lbl = Label(self.frame, text="Delivery or Collection:")
        self.deliv_collect_lbl.grid(column=0, row=6)
        self.this_bkg_dc = Label(self.frame, text=self.this_bkg[0][5])
        self.this_bkg_dc.grid(column=1, row=6)

        self.deliv_collect_lbl = Label(self.frame, text="Delivery or Collection:")
        self.deliv_collect_lbl.grid(column=0, row=6)
        self.this_bkg_dc = Label(self.frame, text=self.this_bkg[0][5])
        self.this_bkg_dc.grid(column=1, row=6)

        # Blank Label to space out details
        self.blank_lbl = Label(self.frame)
        self.blank_lbl.grid(column=3, row=0, padx=50)

        # Display Tool Owner Details
        self.ownr_lbl = Label(self.frame, text="Owner Details")
        self.ownr_lbl.grid(column=4, row=0, padx=20)

        self.ownr_fname_lbl = Label(self.frame, text="First Name:")
        self.ownr_fname_lbl.grid(column=4, row=1)
        self.ownr_fname = Label(self.frame, text=self.tl_owner_usr[0][3])
        self.ownr_fname.grid(column=5, row=1)

        self.ownr_lname_lbl = Label(self.frame, text="Last Name:")
        self.ownr_lname_lbl.grid(column=4, row=2)
        self.ownr_lname = Label(self.frame, text=self.tl_owner_usr[0][4])
        self.ownr_lname.grid(column=5, row=2)

        self.ownr_add_lbl = Label(self.frame, text="Address:")
        self.ownr_add_lbl.grid(column=4, row=3)
        self.ownr_add1 = Label(self.frame, text=self.tl_owner_usr[0][5])
        self.ownr_add1.grid(column=5, row=3)
        self.ownr_add2 = Label(self.frame, text=self.tl_owner_usr[0][6])
        self.ownr_add2.grid(column=5, row=4)
        self.ownr_add3 = Label(self.frame, text=self.tl_owner_usr[0][7])
        self.ownr_add3.grid(column=5, row=5)
        self.ownr_add4 = Label(self.frame, text=self.tl_owner_usr[0][8])
        self.ownr_add4.grid(column=5, row=6)

        self.ownr_pc_lbl = Label(self.frame, text="Post Code:")
        self.ownr_pc_lbl.grid(column=4, row=7)
        self.ownr_pc = Label(self.frame, text=self.tl_owner_usr[0][9])
        self.ownr_pc.grid(column=5, row=7)

        self.ownr_tel_lbl = Label(self.frame, text="Telephone No:")
        self.ownr_tel_lbl.grid(column=4, row=8)
        self.ownr_tel = Label(self.frame, text=self.tl_owner_usr[0][10])
        self.ownr_tel.grid(column=5, row=8)

        self.ownr_id_lbl = Label(self.frame, text="User ID:")
        self.ownr_id_lbl.grid(column=4, row=9)
        self.ownr_id = Label(self.frame, text=self.tl_owner_usr[0][0])
        self.ownr_id.grid(column=5, row=9)

        # Blank Label to space out details
        self.blank_lbl2 = Label(self.frame)
        self.blank_lbl2.grid(column=6, row=0, padx=50)

        # Display Tool User Details
        self.bkr_lbl = Label(self.frame, text="Booker Details")
        self.bkr_lbl.grid(column=7, row=0, padx=20)

        self.bkr_fname_lbl = Label(self.frame, text="First Name:")
        self.bkr_fname_lbl.grid(column=7, row=1)
        self.bkr_fname = Label(self.frame, text=self.bked_by[0][3])
        self.bkr_fname.grid(column=8, row=1)

        self.bkr_lname_lbl = Label(self.frame, text="Last Name:")
        self.bkr_lname_lbl.grid(column=7, row=2)
        self.bkr_lname = Label(self.frame, text=self.bked_by[0][4])
        self.bkr_lname.grid(column=8, row=2)

        self.bkr_add_lbl = Label(self.frame, text="Address:")
        self.bkr_add_lbl.grid(column=7, row=3)
        self.bkr_add1 = Label(self.frame, text=self.bked_by[0][5])
        self.bkr_add1.grid(column=8, row=3)
        self.bkr_add2 = Label(self.frame, text=self.bked_by[0][6])
        self.bkr_add2.grid(column=8, row=4)
        self.bkr_add3 = Label(self.frame, text=self.bked_by[0][7])
        self.bkr_add3.grid(column=8, row=5)
        self.bkr_add4 = Label(self.frame, text=self.bked_by[0][8])
        self.bkr_add4.grid(column=8, row=6)

        self.bkr_pc_lbl = Label(self.frame, text="Post Code:")
        self.bkr_pc_lbl.grid(column=7, row=7)
        self.bkr_pc = Label(self.frame, text=self.bked_by[0][9])
        self.bkr_pc.grid(column=8, row=7)

        self.bkr_tel_lbl = Label(self.frame, text="Telephone No:")
        self.bkr_tel_lbl.grid(column=7, row=8)
        self.bkr_tel = Label(self.frame, text=self.bked_by[0][10])
        self.bkr_tel.grid(column=8, row=8)

        self.bkr_id_lbl = Label(self.frame, text="User ID:")
        self.bkr_id_lbl.grid(column=7, row=9)
        self.bkr_id = Label(self.frame, text=self.bked_by[0][0])
        self.bkr_id.grid(column=8, row=9)

        if self.this_bkg[0][6] != '':
            # Blank Label to space out details
            self.blank_lbl3 = Label(self.frame)
            self.blank_lbl3.grid(column=9, row=0, padx=50)

            # Display Dispatch Rider Details
            self.rdr_lbl = Label(self.frame, text="Dispatch Rider Details")
            self.rdr_lbl.grid(column=10, row=0, padx=20)

            self.rdr_fname_lbl = Label(self.frame, text="First Name:")
            self.rdr_fname_lbl.grid(column=10, row=1)
            self.rdr_fname = Label(self.frame, text=self.cour_usr[0][3])
            self.rdr_fname.grid(column=11, row=1)

            self.rdr_lname_lbl = Label(self.frame, text="Last Name:")
            self.rdr_lname_lbl.grid(column=10, row=2)
            self.rdr_lname = Label(self.frame, text=self.cour_usr[0][4])
            self.rdr_lname.grid(column=11, row=2)

            self.rdr_add_lbl = Label(self.frame, text="Address:")
            self.rdr_add_lbl.grid(column=10, row=3)
            self.rdr_add1 = Label(self.frame, text=self.cour_usr[0][5])
            self.rdr_add1.grid(column=11, row=3)
            self.rdr_add2 = Label(self.frame, text=self.cour_usr[0][6])
            self.rdr_add2.grid(column=11, row=4)
            self.rdr_add3 = Label(self.frame, text=self.cour_usr[0][7])
            self.rdr_add3.grid(column=11, row=5)
            self.rdr_add4 = Label(self.frame, text=self.cour_usr[0][8])
            self.rdr_add4.grid(column=11, row=6)

            self.rdr_pc_lbl = Label(self.frame, text="Post Code:")
            self.rdr_pc_lbl.grid(column=10, row=7)
            self.rdr_pc = Label(self.frame, text=self.cour_usr[0][9])
            self.rdr_pc.grid(column=11, row=7)

            self.rdr_tel_lbl = Label(self.frame, text="Telephone No:")
            self.rdr_tel_lbl.grid(column=10, row=8)
            self.rdr_tel = Label(self.frame, text=self.cour_usr[0][10])
            self.rdr_tel.grid(column=11, row=8)

            self.rdr_id_lbl = Label(self.frame, text="User ID:")
            self.rdr_id_lbl.grid(column=10, row=9)
            self.rdr_id = Label(self.frame, text=self.cour_usr[0][0])
            self.rdr_id.grid(column=11, row=9)

        # Show Completed Status
        if self.this_bkg[0][7] == "Yes":
            self.completed_status = "This Booking is Completed"
        else:
            self.completed_status = "This Booking is Open"
        self.compl_labl = Label(self.frame2, text=self.completed_status, fg='blue')
        self.compl_labl.pack()

        # Shows if return status is late
        if self.this_bkg[0][8] != 0:
            self.no_days_late = str(self.this_bkg[0][8])
            self.late_lbl = Label(self.frame2, text=("Return days late: " + self.no_days_late), fg='red')
            self.late_lbl.pack()

        # Add Condition Details Button
        self.add_cond_btn = Button(self.frame2, text="Add Condition Case with Insurance Company", command=self.add_cond)
        self.add_cond_btn.pack()

        # Tool Owner can add days late, complete the booking and delete the booking
        # This only shows for open bookings and if all condition cases are resolved

        self.unrslved_case = False
        for x in self.cases:
            if x[10] == "No":
                self.unrslved_case = True

        if (self.this_bkg[0][7] == "No") and (self.this_usr[0][2] == "Tool Owner") and (not self.unrslved_case):
            self.dys_late_lbl = Label(self.frame2,
                                      text="Enter Number of Days late the tool was returned (leave blank if none):")
            self.dys_late_lbl.pack()
            self.dys_late_ent = Entry(self.frame2)
            self.dys_late_ent.pack()

            self.compl_btn = Button(self.frame2, text="COMPLETE BOOKING", command=self.complete)
            self.compl_btn.pack()

            self.del_bkg_btn = Button(self.frame2, text="Delete Booking", fg='red', command=self.delete_bkg)
            self.del_bkg_btn.pack()

        if self.unrslved_case:
            self.unrslved_lbl = Label(self.frame2, text="There is an unresolved condition case "
                                                        "being investigated by the insurance company.",
                                      fg='red')
            self.unrslved_lbl.pack()

        # Take Delivery Button appears if courier_id is blank
        if (self.this_usr[0][2] == "Dispatch Rider") and \
                (self.this_bkg[0][5] == "Delivery") and \
                (self.this_bkg[0][6] == ""):
            self.take_deliv_btn = Button(self.frame2, text="Take Delivery", fg='green', command=self.take_deliv)
            self.take_deliv_btn.pack()

    def add_cond(self):
        AddCondition(self.master, self.uid_token, self.slcted_bkg)

    def complete(self):
        if self.dys_late_ent.get() != '':
            late_days = self.dys_late_ent.get()
        else:
            late_days = 0
        SQLUpdate().complete_booking(self.slcted_bkg, 'Yes', late_days)
        self.window.destroy()

    def delete_bkg(self):
        SQLDelete().remove_booking(self.slcted_bkg)
        self.window.destroy()

    def take_deliv(self):
        SQLUpdate().assign_courier(self.slcted_bkg, self.uid_token)
        self.window.destroy()


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    ManageBooking(root, 'to1', 5)
    root.mainloop()

