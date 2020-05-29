from tkinter import *
from Shared_Power.GUI.create_account import CreateAccount
from Shared_Power.GUI.tool_user_view import ToolUserView
from Shared_Power.GUI.tool_owner_view import ToolOwnerView
from Shared_Power.GUI.dispatch_rider_view import DispatchRiderView
from Shared_Power.GUI.insurance_company_view import InsuranceCompanyView
from Shared_Power.DB.sql_read import SQLRead
from Shared_Power.Logs.log import Log


class Welcome:

    def __init__(self, master):
        self.master = master

        self.master.title("Shared Power")

        self.mainframe = Frame(self.master)
        self.mainframe.pack()

        self.frame = Frame(self.mainframe)
        self.frame.pack()

        self.frame2 = Frame(self.mainframe)
        self.frame2.pack()

        self.usr_id_lbl = Label(self.frame, text="User ID")
        self.usr_id_lbl.grid(column=0, row=0)
        self.usr_id_ent = Entry(self.frame)
        self.usr_id_ent.grid(column=1, row=0)

        self.pwrd_lbl = Label(self.frame, text="Password")
        self.pwrd_lbl.grid(column=0, row=1)
        self.pwrd_ent = Entry(self.frame)
        self.pwrd_ent.grid(column=1, row=1)

        self.login_btn = Button(self.frame, text="Log In", command=self.login)
        self.login_btn.grid(column=1, row=2)

        self.create_acc_btn = Button(self.frame, text="Create Account", command=self.create_account)
        self.create_acc_btn.grid(column=1, row=3)

        self.quit_btn = Button(self.frame, text="Quit", command=self.frame.quit)
        self.quit_btn.grid(column=0, row=3)

    def login(self):
        uid = self.usr_id_ent.get()
        pw = self.pwrd_ent.get()
        get_usr = SQLRead().get_user_by_id(uid)

        try:
            real_pw = get_usr[0][1]
            usr_typ = get_usr[0][2]
        except IndexError as e:
            Log().error(e)

        try:
            # Checks variables have been assigned values before running if statement
            real_pw = real_pw
            usr_typ = usr_typ
        except UnboundLocalError as e:
            Log().error(e)
            e_lbl = Label(self.frame2, text="Invalid User ID or Password")
            e_lbl.pack()
        else:
            if pw == real_pw:
                if usr_typ == "Tool User":
                    self.mainframe.destroy()
                    ToolUserView(self.master, uid)
                if usr_typ == "Tool Owner":
                    self.mainframe.destroy()
                    ToolOwnerView(self.master, uid)
                if usr_typ == "Dispatch Rider":
                    self.mainframe.destroy()
                    DispatchRiderView(self.master, uid)
                if usr_typ == "Insurance Company":
                    self.mainframe.destroy()
                    InsuranceCompanyView(self.master, uid)
            else:
                e_lbl = Label(self.frame2, text="Invalid User ID or Password")
                e_lbl.pack()

    def create_account(self):
        CreateAccount(self.master)


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    Welcome(root)
    root.mainloop()
