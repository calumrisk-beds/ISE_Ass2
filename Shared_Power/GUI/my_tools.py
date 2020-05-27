from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.GUI.manage_tool import ManageTool
from Shared_Power.GUI.my_bookings import MyBookings
import Shared_Power.DB.sql_read as sqlr


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class MyTools:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.window = Toplevel()

        self.window.title("My Tools")

        self.frame = Frame(self.window, padx=15, pady=15)
        self.frame.pack(fill=X)

        self.info = Label(self.frame, text="Select Tool")
        self.info.pack()

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

        self.slct_tl_btn = Button(self.frame, text="Manage Tool Properties", command=self.mng_tl)
        self.slct_tl_btn.pack()

        self.view_bkgs_btn = Button(self.frame, text="Manage Tool Bookings", command=self.view_bkgs)
        self.view_bkgs_btn.pack()

    def mng_tl(self):
        # Retrieves selected item and splits the string to retrieve the Tool ID
        selected = self.tls_lstbx.get(ANCHOR)
        selected_tid = selected.split('#')[1]

        # Destroy window
        self.window.destroy()

        # Call ManageTool and pass the value of User ID and Tool ID
        ManageTool(self.master, self.uid_token, selected_tid)

    def view_bkgs(self):
        # Retrieves selected item and splits the string to retrieve the Tool ID
        selected = self.tls_lstbx.get(ANCHOR)
        selected_tid = selected.split('#')[1]

        # Destroy window
        self.window.destroy()

        # Call ManageTool and pass the value of User ID and Tool ID
        MyBookings(self.master, self.uid_token, selected_tid)





if __name__ == "__main__":
    root = Tk()
    CreateTool(root, 'test4')
    root.mainloop()
