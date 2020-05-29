from tkinter import *
from os.path import join, dirname, abspath
import shutil
from PIL import ImageTk, Image
from Shared_Power.DB.sql_read import SQLRead
from Shared_Power.DB.sql_update import SQLUpdate
from Shared_Power.Pool.tool import Tool


class ManageTool:
    def __init__(self, master, uid_token, slcted_tl):
        self.master = master
        self.uid_token = uid_token
        self.slcted_tl = slcted_tl

        self.window = Toplevel()

        self.window.title("Manage Tool")

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

        self.this_tl = SQLRead().get_tool_by_id(self.slcted_tl)
        self.this_usr = SQLRead().get_user_by_id(self.uid_token)

        self.curr_val_lbl = Label(self.frame, text="Current Value", padx=20)
        self.curr_val_lbl.grid(column=1, row=0)

        self.tl_id_lbl = Label(self.frame, text="Tool ID")
        self.tl_id_lbl.grid(column=0, row=1)
        self.this_tl_id = Label(self.frame, text=self.this_tl[0][0])
        self.this_tl_id.grid(column=1, row=1, padx=15)

        self.tl_name_lbl = Label(self.frame, text="Tool Name")
        self.tl_name_lbl.grid(column=0, row=2)
        self.curr_tl_name = Label(self.frame, text=self.this_tl[0][2])
        self.curr_tl_name.grid(column=1, row=2)


        self.descr_lbl = Label(self.frame, text="Description")
        self.descr_lbl.grid(column=0, row=3)
        self.curr_descr = Label(self.frame, text=self.this_tl[0][3])
        self.curr_descr.grid(column=1, row=3)


        self.drate_lbl = Label(self.frame, text="Day Rate")
        self.drate_lbl.grid(column=0, row=4)
        self.curr_drate = Label(self.frame, text=self.this_tl[0][4])
        self.curr_drate.grid(column=1, row=4)


        self.hdrate_lbl = Label(self.frame, text="Half Day Rate")
        self.hdrate_lbl.grid(column=0, row=5)
        self.curr_hdrate = Label(self.frame, text=self.this_tl[0][5])
        self.curr_hdrate.grid(column=1, row=5)


        self.repair_lbl = Label(self.frame, text="Repair Status")
        self.repair_lbl.grid(column=0, row=6)
        self.curr_rstatus = Label(self.frame, text=self.this_tl[0][7])
        self.curr_rstatus.grid(column=1, row=6)


        temp_img = join(dirname(dirname(abspath(__file__))), 'Images/temp_img.jpg')

        with open(temp_img, 'wb') as f:
            f.write(self.this_tl[0][6])

        self.curr_pic_lbl = Label(self.frame2, text="Current Profile Picture")
        self.curr_pic_lbl.pack()
        self.curr_pic = ImageTk.PhotoImage(Image.open(temp_img))
        self.curr_pic_show = Label(self.frame2, image=self.curr_pic)
        self.curr_pic_show.pack()


        if (self.this_usr[0][2] == "Tool Owner") and (self.this_tl[0][1] == self.uid_token):

            self.new_val_lbl = Label(self.frame, text="New Value (leave blank if unchanged)", padx=20)
            self.new_val_lbl.grid(column=2, row=0)
            self.new_tl_name = Entry(self.frame)
            self.new_tl_name.grid(column=2, row=2)
            self.new_descr = Entry(self.frame)
            self.new_descr.grid(column=2, row=3)
            self.new_drate = Entry(self.frame)
            self.new_drate.grid(column=2, row=4)
            self.new_hdrate = Entry(self.frame)
            self.new_hdrate.grid(column=2, row=5)
            self.new_rstatus_var = StringVar()  # Required for Option Menu
            self.new_rstatus_var.set('None')
            self.new_rstatus_opt = OptionMenu(self.frame, self.new_rstatus_var, "None", "In Repair")
            self.new_rstatus_opt.grid(column=2, row=6)
            self.new_pic_lbl = Label(self.frame2, text="New Profile Picture (enter path or leave blank if unchanged)")
            self.new_pic_lbl.pack()
            self.new_pic_path = Entry(self.frame2)
            self.new_pic_path.pack()

            self.chg_btn = Button(self.frame2, text="Make Changes", command=self.update_tool)
            self.chg_btn.pack()



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

    def update_tool(self):
        if self.new_tl_name.get() == '':
            tool_name = self.this_tl[0][2]
        else:
            tool_name = self.new_tl_name.get()

        if self.new_descr.get() == '':
            descr = self.this_tl[0][3]
        else:
            descr = self.new_descr.get()

        if self.new_drate.get() == '':
            day_rate = self.this_tl[0][4]
        else:
            day_rate = self.new_drate.get()

        if self.new_hdrate.get() == '':
            halfd_rate = self.this_tl[0][5]
        else:
            halfd_rate = self.new_hdrate.get()

        if self.new_pic_path.get() == '':
            prof_pic = self.this_tl[0][6]
        else:
            # Copying image file into Images directory as temporary file
            src = self.new_pic_path.get()
            dst = join(dirname(dirname(abspath(__file__))), 'Images')
            temp_store = shutil.copy(src, dst)

            # Read image file as binary file that will be stored into the DB
            f = open(temp_store, 'rb')
            rf = f.read()
            prof_pic = rf

        updated_tl = Tool(tool_id=self.slcted_tl, tool_owner=self.uid_token, tool_name=tool_name,
                          descr=descr, day_rate=day_rate, halfd_rate=halfd_rate,
                          prof_pic=prof_pic, repair_status=self.new_rstatus_var.get())

        SQLUpdate().update_tool(updated_tl)

        self.window.destroy()


if __name__ == "__main__":
    root = Tk()
    ManageTool(root, 'to1', '1')
    root.mainloop()
