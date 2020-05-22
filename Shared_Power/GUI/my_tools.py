from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.create_tool import CreateTool
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.tool import Tool


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class MyTools:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("My Tools")

        self.frame = Frame(self.master, padx=15, pady=15)
        self.frame.pack(fill=X)

        # Create Scrollbar
        self.tls_scrlbar = Scrollbar(self.frame, orient=VERTICAL)

        # Create Tools Listbox
        self.tls_lstbx = Listbox(self.frame, width=50, yscrollcommand=self.tls_scrlbar)

        
        # Configure Scrollbar
        self.tls_scrlbar.config(command=self.tls_lstbx.yview)
        self.tls_scrlbar.pack(side=RIGHT, fill=Y)

        # Pack the Listbox with Scrollbar
        self.tls_lstbx.pack()


        # Call the user's tools
        self.my_tls = sqlr.get_tools_by_uid(self.uid_token)
        for x in self.my_tls:
            self.tl_id = x[0]
            self.tl_name = x[2]
            self.my_tls_short = "#{}# {}".format(str(self.tl_id), self.tl_name)
            self.tls_lstbx.insert(END, self.my_tls_short)


if __name__ == "__main__":
    root = Tk()
    CreateTool(root, 'test4')
    root.mainloop()
