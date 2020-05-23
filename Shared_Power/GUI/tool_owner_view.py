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


class ToolOwnerView:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Tool Owner")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.add_tl_btn = Button(self.frame, text="Add Tool", command=self.add_tool)
        self.add_tl_btn.pack()

        self.mng_tls_btn = Button(self.frame, text="Manage Tool", command=self.mng_tools)
        self.mng_tls_btn.pack()

        # Defining class variable that will be assigned values within functions
        self.ct = ''
        self.mt = ''
        self.mgt = ''

    def add_tool(self):
        self.frame.destroy()

        self.ct = CreateTool(self.master, self.uid_token)

        self.frame = Frame(self.master)
        self.frame.pack(fill=X)

        submit_btn = Button(self.frame, text="Submit", command=self.submit)
        submit_btn.pack(side=RIGHT)

        back_btn = Button(self.frame, text="Back", command=self.back)
        back_btn.pack(side=LEFT)

    def submit(self):
        # Copying image file into Images directory as temporary file
        src = self.ct.pic_path_ent.get()
        dst = join(dirname(dirname(abspath(__file__))), 'Images')
        temp_store = shutil.copy(src, dst)

        # Read image file as binary file that will be stored into the DB
        f = open(temp_store, 'rb')
        rf = f.read()

        # Store tool details in DB
        tl = Tool(tool_id='', tool_owner=self.uid_token, tool_name=self.ct.tl_name_ent.get(),
                  descr=self.ct.descr_ent.get(), day_rate=self.ct.drate_ent.get(),
                  halfd_rate=self.ct.hdrate_ent.get(), prof_pic=rf)
        sqlc.insert_tool(tl)

        # Destroy frames and call tool_owner
        self.ct.frame.destroy()
        self.frame.destroy()
        self.tool_owner()

    def back(self):
        try:
            self.ct.frame.destroy()
        except AttributeError as e:
            print(e)

        try:
            self.ct.mt.destroy()
        except AttributeError as e:
            print(e)

        try:
            self.mgt.frame.destroy()
            self.mgt.frame2.destroy()
        except AttributeError as e:
            print(e)

        self.frame.destroy()

        ToolOwnerView(self.master, self.uid_token)

    def mng_tools(self):
        self.frame.destroy()

        self.mt = MyTools(self.master, self.uid_token)

        self.frame = Frame(self.master)
        self.frame.pack()

        slct_tl_btn = Button(self.frame, text="Select", command=self.select_tool)
        slct_tl_btn.pack()

    def select_tool(self):
        # Retrieves selected item and splits the string to retrieve the Tool ID
        selected = self.mt.tls_lstbx.get(ANCHOR)
        selected_id = selected.split('#')[1]

        # Destroys the MyTools frame and current UserView frame
        self.mt.frame.destroy()
        self.frame.destroy()

        self.frame = Frame(self.master)
        self.frame.pack()

        btn = Button(self.frame, text="Back", command=self.back)
        btn.pack()

        # Call ManageTool and pass the value of User ID and Tool ID
        self.mgt = ManageTool(self.master, self.uid_token, selected_id)

        self.master.mainloop()


if __name__ == "__main__":
    root = Tk()
    ToolOwnerView(root, 'test4')
    root.mainloop()
