from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
import Shared_Power.DB.sql_create as sqlc
from Shared_Power.Classes.tool import Tool
# from Shared_Power.GUI.user_view import UserView

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


if __name__ == "__main__":
    root = Tk()
    CreateTool(root, 'test4')
    root.mainloop()
