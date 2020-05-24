from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.GUI.my_tools import MyTools
from Shared_Power.GUI.manage_tool import ManageTool
from Shared_Power.GUI.book_tool import BookTool
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool
from Shared_Power.Classes.booking import Booking

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()


class ToolDetails:
    def __init__(self, master, uid_token, slcted_tl):
        self.master = master
        self.uid_token = uid_token
        self.slcted_tl = slcted_tl

        self.master.title("Tool Details")

        self.mainframe = Frame(self.master)
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

        # Fetch Tool from DB
        self.this_tl = sqlr.get_tool_by_id(slcted_tl)

        # Fetch Tool Owner from DB
        tl_owner = self.this_tl[0][1]
        self.tl_owner_usr = sqlr.get_user_by_id(tl_owner)

        # Display Tool Details
        self.tl_lbl = Label(self.frame, text="Tool Details")
        self.tl_lbl.grid(column=0, row=0, padx=20)

        self.tl_id_lbl = Label(self.frame, text="Tool ID")
        self.tl_id_lbl.grid(column=0, row=1)
        self.this_tl_id = Label(self.frame, text=self.this_tl[0][0])
        self.this_tl_id.grid(column=1, row=1)

        self.tl_name_lbl = Label(self.frame, text="Tool Name")
        self.tl_name_lbl.grid(column=0, row=2)
        self.this_tl_name = Label(self.frame, text=self.this_tl[0][2])
        self.this_tl_name.grid(column=1, row=2)

        self.descr_lbl = Label(self.frame, text="Description")
        self.descr_lbl.grid(column=0, row=3)
        self.this_descr = Label(self.frame, text=self.this_tl[0][3])
        self.this_descr.grid(column=1, row=3)

        self.drate_lbl = Label(self.frame, text="Day Rate")
        self.drate_lbl.grid(column=0, row=4)
        self.this_drate = Label(self.frame, text=self.this_tl[0][4])
        self.this_drate.grid(column=1, row=4)

        self.hdrate_lbl = Label(self.frame, text="Half Day Rate")
        self.hdrate_lbl.grid(column=0, row=5)
        self.this_hdrate = Label(self.frame, text=self.this_tl[0][5])
        self.this_hdrate.grid(column=1, row=5)

        # Blank Label to space out details
        self.blank_lbl = Label(self.frame)
        self.blank_lbl.grid(column=3, row=0, padx=50)

        # Display Tool Owner Details
        self.usr_lbl = Label(self.frame, text="Owner Details")
        self.usr_lbl.grid(column=4, row=0, padx=20)

        self.fname_lbl = Label(self.frame, text="First Name:")
        self.fname_lbl.grid(column=4, row=1)
        self.fname = Label(self.frame, text=self.tl_owner_usr[0][3])
        self.fname.grid(column=5, row=1)

        self.lname_lbl = Label(self.frame, text="Last Name:")
        self.lname_lbl.grid(column=4, row=2)
        self.lname = Label(self.frame, text=self.tl_owner_usr[0][4])
        self.lname.grid(column=5, row=2)

        self.add_lbl = Label(self.frame, text="Address:")
        self.add_lbl.grid(column=4, row=3)
        self.add1 = Label(self.frame, text=self.tl_owner_usr[0][5])
        self.add1.grid(column=5, row=3)
        self.add2 = Label(self.frame, text=self.tl_owner_usr[0][6])
        self.add2.grid(column=5, row=4)
        self.add3 = Label(self.frame, text=self.tl_owner_usr[0][7])
        self.add3.grid(column=5, row=5)
        self.add4 = Label(self.frame, text=self.tl_owner_usr[0][8])
        self.add4.grid(column=5, row=6)

        self.pc_lbl = Label(self.frame, text="Post Code:")
        self.pc_lbl.grid(column=4, row=7)
        self.pc = Label(self.frame, text=self.tl_owner_usr[0][9])
        self.pc.grid(column=5, row=7)

        self.tel_lbl = Label(self.frame, text="Telephone No:")
        self.tel_lbl.grid(column=4, row=8)
        self.tel = Label(self.frame, text=self.tl_owner_usr[0][10])
        self.tel.grid(column=5, row=8)


        # Display Tool Profile Picture in new frame
        temp_img = join(dirname(dirname(abspath(__file__))), 'Images/temp_img.jpg')

        with open(temp_img, 'wb') as f:
            f.write(self.this_tl[0][6])

        self.curr_pic_lbl = Label(self.frame2, text="Profile Picture")
        self.curr_pic_lbl.pack()
        self.curr_pic = ImageTk.PhotoImage(Image.open(temp_img))
        self.curr_pic_show = Label(self.frame2, image=self.curr_pic)
        self.curr_pic_show.pack()

        self.chk_btn = Button(self.frame3, text="Check Availability", command=self.check_available)
        self.chk_btn.pack(fill=X)

        self.interior.bind('<Configure>', self._configure_interior)
        self.canv.bind('<Configure>', self._configure_canvas)

        # Class variables
        self.bt = ''

        mainloop()

    def check_available(self):
        self.mainframe.destroy()
        self.bt = BookTool(self.master, self.uid_token, self.slcted_tl)


    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canv.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canv.winfo_width():
        # update the canvas's width to fit the inner frame
            self.canv.config(width=self.interior.winfo_reqwidth())



    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canv.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canv.itemconfigure(self.interior_id, width=self.canv.winfo_width())





if __name__ == "__main__":
    root = Tk()
    ToolDetails(root, 'test4', 4)
    root.mainloop()