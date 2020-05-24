from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.GUI.my_tools import MyTools
from Shared_Power.GUI.manage_tool import ManageTool
from Shared_Power.GUI.view_tools import ViewTools
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool
from Shared_Power.Classes.booking import Booking

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()


class ToolUserView:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Tool User")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.vw_tl_btn = Button(self.frame, text="Book Tool", command=self.vw_tools)
        self.vw_tl_btn.pack()

        #self.mng_bkgs_btn = Button(self.frame, text="Manage Tool", command=self.manage_bookings)
        #self.mng_bkgs_btn.pack()

        # Defining class variable that will be assigned values within functions
        self.vt = ''

    def vw_tools(self):
        # Destroy frame
        self.frame.destroy()

        # Call ViewTolls
        self.vt = ViewTools(self.master, self.uid_token)

    def select_tool(self):
        # Retrieves selected item and splits the string to retrieve the Tool ID
        selected = self.vt.tls_lstbx.get(ANCHOR)
        selected_id = selected.split('#')[1]
        print(selected_id)


if __name__ == "__main__":
    root = Tk()
    ToolUserView(root, 'test4')
    root.mainloop()
