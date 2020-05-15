from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
from Shared_Power.GUI.create_account import CreateAccount
import Shared_Power.DB.sql_backend as sql


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class UserView:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

    def tool_user(self):
        print("test")

    def tool_owner(self):
        pass

    def dispatch_rider(self):
        pass

    def ins_comp(self):
        pass

    def sys_admin(self):
        pass

    def add_tool(self):
        pass

    def mang_tools(self):
        pass

    def view_tools(self):
        pass

    def book_tool(self):
        pass

    def mang_bkings(self):
        pass
