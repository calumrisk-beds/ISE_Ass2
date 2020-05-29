from tkinter import *
from os.path import join, dirname, abspath
import shutil
from Shared_Power.DB.sql_create import SQLCreate
from Shared_Power.Pool.tool import Tool

class CreateTool:
    """Called by Tool Owner to create a tool.
        Tk() is passed into master from previous class, allowing main Tkinter window to run.
        The user's ID is passed into uid_token."""

    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        # New windows
        self.window = Toplevel()

        # Window title
        self.window.title("Create Tool")

        # Uses a main frame for other frames to be packed into
        self.mainframe = Frame(self.window)
        self.mainframe.pack()

        # Frame packed into Main Frame
        self.frame = Frame(self.mainframe)
        self.frame.pack()

        # Frame 2 packed into Main Frame
        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        # Various Labels and Entry Boxes to capture details

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

        self.submit_btn = Button(self.frame2, text="Submit", command=self.submit)
        self.submit_btn.pack()

    def submit(self):
        """Called when submit button is selected"""
        # Copying image file into Images directory as temporary file
        src = self.pic_path_ent.get()
        dst = join(dirname(dirname(abspath(__file__))), 'Images')
        temp_store = shutil.copy(src, dst)

        # Read image file as binary file that will be stored into the DB
        f = open(temp_store, 'rb')
        rf = f.read()

        # Temporary instance of Tool to capture data
        tl = Tool(tool_id='', tool_owner=self.uid_token, tool_name=self.tl_name_ent.get(),
                  descr=self.descr_ent.get(), day_rate=self.drate_ent.get(),
                  halfd_rate=self.hdrate_ent.get(), prof_pic=rf, repair_status='None')

        # Store instance of Tool in table of DB
        SQLCreate().insert_tool(tl)

        # Destroy window
        self.window.destroy()


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    CreateTool(root, 'test4')
    root.mainloop()
