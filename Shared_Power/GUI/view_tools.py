from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
import datetime
from Shared_Power.GUI.tool_details import ToolDetails
import Shared_Power.DB.sql_read as sqlr

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)

logfile = join(dirname(dirname(abspath(__file__))), 'LogFile.txt')
now = datetime.datetime.now()


class ViewTools:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.window = Toplevel()

        self.window.title("View Tools")

        self.frame = Frame(self.window, padx=15, pady=15)
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

        # Call all tools and add them to the Listbox
        self.all_tls = sqlr.get_all_tools()
        for x in self.all_tls:
            self.tl_id = x[0]
            self.tl_name = x[2]
            self.all_tls_short = "#{}# {}".format(str(self.tl_id), self.tl_name)
            self.tls_lstbx.insert(END, self.all_tls_short)

        self.slct_tl_btn = Button(self.frame, text="Select", command=self.select_tool)
        self.slct_tl_btn.pack()

        # Class variables
        self.td = ''
        self.ta = ''

    def select_tool(self):
        # Retrieves selected item and splits the string to retrieve the Tool ID
        selected = self.tls_lstbx.get(ANCHOR)
        selected_tl = selected.split('#')[1]

        # Destroys the window
        self.window.destroy()

        # Call ToolDetails
        self.td = ToolDetails(self.master, self.uid_token, selected_tl)

if __name__ == "__main__":
    root = Tk()
    ViewTools(root, 'test4')
    root.mainloop()