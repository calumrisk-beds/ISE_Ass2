from tkinter import *
import sqlite3
from os.path import join, dirname, abspath
import Shared_Power.DB.sql_create as sqlc
from Shared_Power.Classes.user import User

path = join(dirname(dirname(abspath(__file__))), 'DB/shared_power.db')
conn = sqlite3.connect(path)


class CreateAccount:
    def __init__(self, master):
        self.master = master
        self.master.title("Create Account")

        self.frame = Frame(master)
        self.frame.pack()

        self.usr_id_lbl = Label(self.frame, text="User ID")
        self.usr_id_lbl.grid(column=0, row=0)
        self.usr_id_ent = Entry(self.frame)
        self.usr_id_ent.grid(column=1, row=0)

        self.pwrd_lbl = Label(self.frame, text="Password")
        self.pwrd_lbl.grid(column=0, row=1)
        self.pwrd_ent = Entry(self.frame)
        self.pwrd_ent.grid(column=1, row=1)

        self.usr_typ_lbl = Label(self.frame, text="User Type")
        self.usr_typ_lbl.grid(column=0, row=2)
        self.usr_typ_var = StringVar()  # Required for Option Menu
        self.usr_typ_var.set('Tool User')
        self.usr_typ_opt = OptionMenu(self.frame, self.usr_typ_var, "Tool User", "Tool Owner", "Dispatch Rider")
        self.usr_typ_opt.grid(column=1, row=2)

        self.fname_lbl = Label(self.frame, text="First Name")
        self.fname_lbl.grid(column=0, row=3)
        self.fname_ent = Entry(self.frame)
        self.fname_ent.grid(column=1, row=3)

        self.lname_lbl = Label(self.frame, text="Last Name")
        self.lname_lbl.grid(column=0, row=4)
        self.lname_ent = Entry(self.frame)
        self.lname_ent.grid(column=1, row=4)

        self.add1_lbl = Label(self.frame, text="Address Line 1")
        self.add1_lbl.grid(column=0, row=5)
        self.add1_ent = Entry(self.frame)
        self.add1_ent.grid(column=1, row=5)

        self.add2_lbl = Label(self.frame, text="Address Line 2")
        self.add2_lbl.grid(column=0, row=6)
        self.add2_ent = Entry(self.frame)
        self.add2_ent.grid(column=1, row=6)

        self.add3_lbl = Label(self.frame, text="Address Line 3")
        self.add3_lbl.grid(column=0, row=7)
        self.add3_ent = Entry(self.frame)
        self.add3_ent.grid(column=1, row=7)

        self.add4_lbl = Label(self.frame, text="Address Line 4")
        self.add4_lbl.grid(column=0, row=8)
        self.add4_ent = Entry(self.frame)
        self.add4_ent.grid(column=1, row=8)

        self.pc_lbl = Label(self.frame, text="Post Code")
        self.pc_lbl.grid(column=0, row=9)
        self.pc_ent = Entry(self.frame)
        self.pc_ent.grid(column=1, row=9)

        self.tel_lbl = Label(self.frame, text="Telephone Number")
        self.tel_lbl.grid(column=0, row=10)
        self.tel_ent = Entry(self.frame)
        self.tel_ent.grid(column=1, row=10)

        self.quit_btn = Button(self.frame, text="Quit", command=self.frame.quit)
        self.quit_btn.grid(column=0, row=11)

        self.submit_btn = Button(self.frame, text="Submit", command=self.submit)
        self.submit_btn.grid(column=1, row=11)


    def submit(self):
        # Insert into DB
        usr = User(self.usr_id_ent.get(), self.pwrd_ent.get(), self.usr_typ_var.get(), self.fname_ent.get(),
                   self.lname_ent.get(), self.add1_ent.get(), self.add2_ent.get(), self.add3_ent.get(),
                   self.add4_ent.get(), self.pc_ent.get(), self.tel_ent.get(), 0)
        sqlc.insert_user(usr)

        # Clear Text Boxes
        self.usr_id_ent.delete(0, END)
        self.pwrd_ent.delete(0, END)
        self.fname_ent.delete(0, END)
        self.lname_ent.delete(0, END)
        self.add1_ent.delete(0, END)
        self.add2_ent.delete(0, END)
        self.add3_ent.delete(0, END)
        self.add4_ent.delete(0, END)
        self.pc_ent.delete(0, END)
        self.tel_ent.delete(0, END)



if __name__ == "__main__":
    root = Tk()
    CreateAccount(root)
    root.mainloop()

