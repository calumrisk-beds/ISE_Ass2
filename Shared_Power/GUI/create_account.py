from tkinter import *
from Shared_Power.DB.sql_create import SQLCreate
from Shared_Power.Pool.user import User


class CreateAccount:
    """Enables account creation for Tool Owner, Tool User and Dispatch Rider.
        A system administrator must create Insurance Company accounts.
        Tk() is passed into master from previous class, allowing main Tkinter windows to run."""

    def __init__(self, master):
        self.master = master

        # New window
        self.window = Toplevel()

        # Window title
        self.window.title("Create Account")

        # Frame packed into window
        self.frame = Frame(self.window)
        self.frame.pack()

        # Various Labels and Entry Boxes to capture user details

        self.usr_id_lbl = Label(self.frame, text="User ID")
        self.usr_id_lbl.grid(column=0, row=0)  # Grid format specifies position based on column and row
        self.usr_id_ent = Entry(self.frame)
        self.usr_id_ent.grid(column=1, row=0)

        self.pwrd_lbl = Label(self.frame, text="Password")
        self.pwrd_lbl.grid(column=0, row=1)
        self.pwrd_ent = Entry(self.frame)
        self.pwrd_ent.grid(column=1, row=1)

        # Option Menu for User Type
        self.usr_typ_lbl = Label(self.frame, text="User Type")
        self.usr_typ_lbl.grid(column=0, row=2)
        self.usr_typ_var = StringVar()  # Required for Option Menu
        self.usr_typ_var.set('Tool User')  # Default value set
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
        """Called when submit button is selected."""
        # Temporary instance of User to store captured data
        usr = User(self.usr_id_ent.get(), self.pwrd_ent.get(), self.usr_typ_var.get(), self.fname_ent.get(),
                   self.lname_ent.get(), self.add1_ent.get(), self.add2_ent.get(), self.add3_ent.get(),
                   self.add4_ent.get(), self.pc_ent.get(), self.tel_ent.get())
        # Insert instance of User into table of DB
        SQLCreate().insert_user(usr)

        # Destroy window
        self.window.destroy()


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    CreateAccount(root)
    root.mainloop()

