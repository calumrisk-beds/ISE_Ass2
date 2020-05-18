from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
import Shared_Power.DB.sql_create as sqlc
from Shared_Power.Classes.tool import Tool

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class CreateTool:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Create Tool")

        self.frame = Frame(master)
        self.frame.pack()

        self.tl_name_lbl = Label(self.frame, text="Tool Name")
        self.tl_name_lbl.grid(column=0, row=0)
        self.tl_name_ent = Entry(self.frame)
        self.tl_name_ent.grid(column=1, row=0)

        self.descr_lbl = Label(self.frame, text="Description")
        self.descr_lbl.grid(column=0, row=1)
        self.descr_ent = Entry(self.frame)
        self.descr_ent.grid(column=1, row=1)

        self.drate_lbl = Label(self.frame, text="Day Rate")
        self.drate_lbl.grid(column=0, row=2)
        self.drate_ent = Entry(self.frame)
        self.drate_ent.grid(column=1, row=2)

        self.hdrate_lbl = Label(self.frame, text="Half Day Rate")
        self.hdrate_lbl.grid(column=0, row=3)
        self.hdrate_ent = Entry(self.frame)
        self.hdrate_ent.grid(column=1, row=3)

        self.pic_path_lbl = Label(self.frame, text="Profile Picture (enter file path)")
        self.pic_path_lbl.grid(column=0, row=4)
        self.pic_path_ent = Entry(self.frame)
        self.pic_path_ent.grid(column=1, row=4)

        self.submit_btn = Button(self.frame, text="Submit", command=self.submit)
        self.submit_btn.grid(column=1, row=5)

    def submit(self):
        # Copying image file into Images directory as temporary file
        src = self.pic_path_ent.get()
        dst = join(dirname(dirname(abspath(__file__))), 'Images')
        temp_store = shutil.copy(src, dst)

        # Read image file as binary file that will be stored into the DB
        f = open(temp_store, 'rb')
        rf = f.read()

        # Store tool details in DB
        tl = Tool(tool_id='', tool_owner=self.uid_token, tool_name=self.tl_name_ent.get(), descr=self.descr_ent.get(),
                  day_rate=self.drate_ent.get(), halfd_rate=self.hdrate_ent.get(), prof_pic=rf)
        sqlc.insert_tool(tl)

        # Clear Text Boxes
        self.tl_name_ent.delete(0, END)
        self.descr_ent.delete(0, END)
        self.drate_ent.delete(0, END)
        self.hdrate_ent.delete(0, END)
        self.pic_path_ent.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    CreateTool(root)
    root.mainloop()
