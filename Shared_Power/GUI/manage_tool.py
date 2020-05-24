from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
from PIL import ImageTk, Image
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class ManageTool:
    def __init__(self, master, uid_token, slcted_tl):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Manage Tool")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.frame2 = Frame(self.master)
        self.frame2.pack()

        self.this_tl = sqlr.get_tool_by_id(slcted_tl)

        #self.this_tl_id_txt = "Tool ID: #{}#".format(self.this_tl[0][0])

        self.curr_val_lbl = Label(self.frame, text="Current Value", padx=20)
        self.curr_val_lbl.grid(column=1, row=0)

        self.new_val_lbl = Label(self.frame, text="New Value (leave blank if unchanged)", padx=20)
        self.new_val_lbl.grid(column=2, row=0)

        self.tl_id_lbl = Label(self.frame, text="Tool ID")
        self.tl_id_lbl.grid(column=0, row=1)
        self.this_tl_id = Label(self.frame, text=self.this_tl[0][0])
        self.this_tl_id.grid(column=1, row=1, padx=15)

        self.tl_name_lbl = Label(self.frame, text="Tool Name")
        self.tl_name_lbl.grid(column=0, row=2)
        self.curr_tl_name = Label(self.frame, text=self.this_tl[0][2])
        self.curr_tl_name.grid(column=1, row=2)
        self.new_tl_name = Entry(self.frame)
        self.new_tl_name.grid(column=2, row=2)

        self.descr_lbl = Label(self.frame, text="Description")
        self.descr_lbl.grid(column=0, row=3)
        self.curr_descr = Label(self.frame, text=self.this_tl[0][3])
        self.curr_descr.grid(column=1, row=3)
        self.new_descr = Entry(self.frame)
        self.new_descr.grid(column=2, row=3)

        self.drate_lbl = Label(self.frame, text="Day Rate")
        self.drate_lbl.grid(column=0, row=4)
        self.curr_drate = Label(self.frame, text=self.this_tl[0][4])
        self.curr_drate.grid(column=1, row=4)
        self.new_drate = Entry(self.frame)
        self.new_drate.grid(column=2, row=4)

        self.hdrate_lbl = Label(self.frame, text="Half Day Rate")
        self.hdrate_lbl.grid(column=0, row=5)
        self.curr_hdrate = Label(self.frame, text=self.this_tl[0][5])
        self.curr_hdrate.grid(column=1, row=5)
        self.new_hdrate = Entry(self.frame)
        self.new_hdrate.grid(column=2, row=5)

        temp_img = join(dirname(dirname(abspath(__file__))), 'Images/temp_img.jpg')

        with open(temp_img, 'wb') as f:
            f.write(self.this_tl[0][6])

        self.curr_pic_lbl = Label(self.frame2, text="Current Profile Picture")
        self.curr_pic_lbl.pack()
        self.curr_pic = ImageTk.PhotoImage(Image.open(temp_img))
        self.curr_pic_show = Label(self.frame2, image=self.curr_pic)
        self.curr_pic_show.pack()
        self.new_pic_lbl = Label(self.frame2, text="New Profile Picture (enter path or leave blank if unchanged)")
        self.new_pic_lbl.pack()
        self.new_pic_ent = Entry(self.frame2)
        self.new_pic_ent.pack()


if __name__ == "__main__":
    root = Tk()
    ManageTool(root, 'test4', '4')
    root.mainloop()
