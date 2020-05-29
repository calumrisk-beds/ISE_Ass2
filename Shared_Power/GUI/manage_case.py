from tkinter import *
from os.path import join, dirname, abspath
from PIL import ImageTk, Image
from Shared_Power.DB.sql_read import SQLRead
from Shared_Power.DB.sql_update import SQLUpdate
from Shared_Power.Pool.case import Case
from Shared_Power.GUI.manage_tool import ManageTool
from Shared_Power.GUI.manage_booking import ManageBooking


class ManageCase:
    def __init__(self, master, uid_token, slcted_case):
        self.master = master
        self.uid_token = uid_token
        self.slcted_case = slcted_case

        self.window = Toplevel()

        self.window.title("Manage Case")

        self.mainframe = Frame(self.window)
        self.mainframe.pack(expand=True, fill=BOTH)

        self.scrlbar = Scrollbar(self.mainframe, orient=VERTICAL)
        self.scrlbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        self.canv = Canvas(self.mainframe, bd=0, highlightthickness=0, yscrollcommand=self.scrlbar)
        self.canv.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.scrlbar.config(command=self.canv.yview)

        self.canv.xview_moveto(0)
        self.canv.yview_moveto(0)

        self.interior = Frame(self.canv)
        self.interior_id = self.canv.create_window(0, 0, window=self.interior, anchor=NW)

        self.frame = Frame(self.interior)
        self.frame.pack()

        self.frame2 = Frame(self.interior)
        self.frame2.pack()

        self.frame3 = Frame(self.interior)
        self.frame3.pack()

        # Fetch required details from DB
        self.this_case = SQLRead().get_case_by_id(self.slcted_case)
        self.bkg_id = self.this_case[0][2]
        self.this_bkg = SQLRead().get_booking_by_id(self.bkg_id)
        self.tl_id = self.this_bkg[0][1]
        self.notes = self.this_case[0][3]
        self.rslved_state = self.this_case[0][10]

        # Details of case

        self.case_id_lbl = Label(self.frame, text="Case ID:", padx=20)
        self.case_id_lbl.grid(column=0, row=0)
        self.show_case_id = Label(self.frame, text=str(self.slcted_case))
        self.show_case_id.grid(column=1, row=0)

        self.tl_id_lbl = Label(self.frame, text="Tool ID:", padx=20)
        self.tl_id_lbl.grid(column=0, row=1)
        self.show_tl_id = Label(self.frame, text=str(self.tl_id))
        self.show_tl_id.grid(column=1, row=1)

        self.bkg_id_lbl = Label(self.frame, text="Booking ID:", padx=20)
        self.bkg_id_lbl.grid(column=0, row=2)
        self.show_bkg_id = Label(self.frame, text=str(self.bkg_id))
        self.show_bkg_id.grid(column=1, row=2)

        self.notes_lbl = Label(self.frame, text="Notes:", padx=20)
        self.notes_lbl.grid(column=0, row=3)
        self.show_notes = Label(self.frame, text=str(self.notes))
        self.show_notes.grid(column=1, row=3)


        self.fault_lbl = Label(self.frame, text="User ID at fault or your User ID if you are to pay:", padx=20)
        self.fault_lbl.grid(column=0, row=4)
        if self.rslved_state == "No":
            self.fault_ent = Entry(self.frame)
            self.fault_ent.grid(column=1, row=4)
        else:
            self.show_fault = Label(self.frame, text=str(self.this_case[0][8]))
            self.show_fault.grid(column=1, row=4)

        self.dmg_lbl = Label(self.frame, text="Damage Charge (£):", padx=20)
        self.dmg_lbl.grid(column=0, row=5)
        if self.rslved_state == "No":
            self.dmg_ent = Entry(self.frame)
            self.dmg_ent.grid(column=1, row=5)
        else:
            self.show_dmg = Label(self.frame, text=str(self.this_case[0][9]))
            self.show_dmg.grid(column=1, row=5)

        # Option Menu for Resolved
        self.resolved_lbl = Label(self.frame, text="Resolved:")
        self.resolved_lbl.grid(column=0, row=6)
        if self.rslved_state == "No":
            self.resolved_var = StringVar()  # Required for Option Menu
            self.resolved_var.set('No')  # Default value set
            self.resolved_opt = OptionMenu(self.frame, self.resolved_var, "No", "Yes")
            self.resolved_opt.grid(column=1, row=6)
        else:
            self.show_resolved = Label(self.frame, text=str(self.this_case[0][10]))
            self.show_resolved.grid(column=1, row=6)

        if self.rslved_state == "No":
            self.submit = Button(self.frame2, text="Submit Changes", command=self.submit)
            self.submit.pack()

        self.mng_tool_btn = Button(self.frame2, text="Show Tool Detail", command=self.tool_details)
        self.mng_tool_btn.pack()

        self.mng_bkg_btn = Button(self.frame2, text="Show Booking Detail", command=self.booking_details)
        self.mng_bkg_btn.pack()

        # Load Images

        self.photo1 = self.this_case[0][4]
        self.photo2 = self.this_case[0][5]
        self.photo3 = self.this_case[0][6]
        self.photo4 = self.this_case[0][7]

        temp_img1 = join(dirname(dirname(abspath(__file__))), 'Images/temp_img1.jpg')

        with open(temp_img1, 'wb') as f:
            f.write(self.photo1)

        temp_img2 = join(dirname(dirname(abspath(__file__))), 'Images/temp_img2.jpg')

        with open(temp_img2, 'wb') as f:
            f.write(self.photo2)

        temp_img3 = join(dirname(dirname(abspath(__file__))), 'Images/temp_img3.jpg')

        with open(temp_img3, 'wb') as f:
            f.write(self.photo3)

        temp_img4 = join(dirname(dirname(abspath(__file__))), 'Images/temp_img4.jpg')

        with open(temp_img4, 'wb') as f:
            f.write(self.photo4)

        self.pic_lbl = Label(self.frame3, text="Pictures")
        self.pic_lbl.pack()
        self.pic1 = ImageTk.PhotoImage(Image.open(temp_img1))
        self.pic1_show = Label(self.frame3, image=self.pic1)
        self.pic1_show.pack()
        self.pic2 = ImageTk.PhotoImage(Image.open(temp_img2))
        self.pic2_show = Label(self.frame3, image=self.pic2)
        self.pic2_show.pack()
        self.pic3 = ImageTk.PhotoImage(Image.open(temp_img3))
        self.pic3_show = Label(self.frame3, image=self.pic3)
        self.pic3_show.pack()
        self.pic4 = ImageTk.PhotoImage(Image.open(temp_img4))
        self.pic4_show = Label(self.frame3, image=self.pic4)
        self.pic4_show.pack()

        self.interior.bind('<Configure>', self._configure_interior)
        self.canv.bind('<Configure>', self._configure_canvas)

        mainloop()

    # track changes to the canvas and frame width and sync them, also updating the scrollbar
    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canv.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canv.winfo_width():
            # Update the canvas's width to fit the inner frame
            self.canv.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canv.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canv.itemconfigure(self.interior_id, width=self.canv.winfo_width())

    def submit(self):
        """Called when submit button is entered."""
        # Temporarily assigns retrieved values to Case object
        case = Case(case_id=self.slcted_case, tool_id=self.tl_id, booking_id=self.bkg_id, notes=self.notes,
                    photo1=self.photo1, photo2=self.photo2, photo3=self.photo3, photo4=self.photo4,
                    at_fault=self.fault_ent.get(), damage_charge=self.dmg_ent.get(), resolved=self.resolved_var.get())

        # Updates entry in cases table in DB
        SQLUpdate().update_case(case)

        # Close window
        self.window.destroy()

    def tool_details(self):
        ManageTool(self.master, self.uid_token, self.tl_id)

    def booking_details(self):
        ManageBooking(self.master, self.uid_token, self.bkg_id)




if __name__ == "__main__":
    root = Tk()
    ManageCase(root, 'insurecomp1', '1')
    root.mainloop()
