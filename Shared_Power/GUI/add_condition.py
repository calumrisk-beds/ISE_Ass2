from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import shutil
from PIL import ImageTk, Image
import Shared_Power.DB.sql_create as sqlc
import Shared_Power.DB.sql_read as sqlr
from Shared_Power.Classes.condition import Condition


path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class AddCondition:
    def __init__(self, master, uid_token, slcted_bkg):
        self.master = master
        self.uid_token = uid_token
        self.slcted_bkg = slcted_bkg

        self.window = Toplevel()

        self.window.title("Add Condition Details")

        self.mainframe = Frame(self.window)
        self.mainframe.pack()

        self.frame = Frame(self.mainframe)
        self.frame.pack()

        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        self.frame3 = Frame(self.mainframe)
        self.frame3.pack()

        # Call the booking
        self.this_bkg = sqlr.get_booking_by_id(self.slcted_bkg)

        self.cond_lbl = Label(self.frame, text=("Add Condition Details for Booking ID: " + str(self.slcted_bkg)))
        self.cond_lbl.pack()

        self.notes_lbl = Label(self.frame2, text="Notes:")
        self.notes_lbl.grid(column=0, row=0, padx=20)
        self.notes_ent = Entry(self.frame2, width=100)
        self.notes_ent.grid(column=1, row=0)

        self.pic_path_lbl = Label(self.frame2, text="Photos (enter file path)")
        self.pic_path_lbl.grid(column=0, row=1)
        self.pic1_path_ent = Entry(self.frame2, width=50)
        self.pic1_path_ent.grid(column=1, row=1)
        self.pic2_path_ent = Entry(self.frame2, width=50)
        self.pic2_path_ent.grid(column=1, row=2)
        self.pic3_path_ent = Entry(self.frame2, width=50)
        self.pic3_path_ent.grid(column=1, row=3)
        self.pic4_path_ent = Entry(self.frame2, width=50)
        self.pic4_path_ent.grid(column=1, row=4)

        self.submit_btn = Button(self.frame3, text="Submit", command=self.submit)
        self.submit_btn.pack()

    def submit(self):
        # Copying image files into Images directory as temporary files
        src1 = self.pic1_path_ent.get()
        src2 = self.pic2_path_ent.get()
        src3 = self.pic3_path_ent.get()
        src4 = self.pic4_path_ent.get()
        dst = join(dirname(dirname(abspath(__file__))), 'Images')
        temp_store1 = shutil.copy(src1, dst)
        temp_store2 = shutil.copy(src2, dst)
        temp_store3 = shutil.copy(src3, dst)
        temp_store4 = shutil.copy(src4, dst)

        # Read image files as binary file that will be stored into the DB
        f1 = open(temp_store1, 'rb')
        rf1 = f1.read()
        f2 = open(temp_store2, 'rb')
        rf2 = f2.read()
        f3 = open(temp_store3, 'rb')
        rf3 = f3.read()
        f4 = open(temp_store4, 'rb')
        rf4 = f4.read()

        # Store condition details in DB
        clog = Condition(log_id='', tool_id=self.this_bkg[0][1], booking_id=self.slcted_bkg,
                        notes=self.notes_ent.get(), photo1=rf1, photo2=rf2, photo3=rf3, photo4=rf4)

        sqlc.insert_condition_log(clog)

        # Destroy window
        self.window.destroy()

