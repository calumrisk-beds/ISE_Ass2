from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.GUI.my_tools import MyTools
from Shared_Power.GUI.manage_tool import ManageTool
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class UserView:

    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.frame = Frame(self.master)
        self.frame.pack()

    def tool_user(self):
        print("test")

    def dispatch_rider(self):
        pass

    def ins_comp(self):
        pass

    def sys_admin(self):
        pass

    def view_tools(self):
        pass

    def book_tool(self):
        pass

    def mang_bkings(self):
        pass




if __name__ == "__main__":
    root = Tk()
    UserView(root, 'test4').tool_owner()
    root.mainloop()
