from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
import Shared_Power.DB.sql_create as sql


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class UserView:

    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.frame = Frame(master)
        self.frame.pack()

    def tool_user(self):
        print("test")

    def tool_owner(self):
        self.master.title("Tool Owner")

        add_tl_btn = Button(self.frame, text="Add Tool", command=self.add_tool)
        add_tl_btn.grid(column=0, row=0)

    def dispatch_rider(self):
        pass

    def ins_comp(self):
        pass

    def sys_admin(self):
        pass

    def add_tool(self):
        self.frame.destroy()
        CreateTool(self.master, self.uid_token)

    def mang_tools(self):
        pass

    def view_tools(self):
        pass

    def book_tool(self):
        pass

    def mang_bkings(self):
        pass
