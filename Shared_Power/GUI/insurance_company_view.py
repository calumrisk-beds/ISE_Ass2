from tkinter import *
from Shared_Power.GUI.my_invoices import MyInvoices
from Shared_Power.GUI.view_cases import ViewCases


class InsuranceCompanyView:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Insurance Company")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.my_delivs_btn = Button(self.frame, text="Open Cases", command=self.opn_cases)
        self.my_delivs_btn.pack()

        self.my_delivs_btn = Button(self.frame, text="Closed Cases", command=self.clsd_cases)
        self.my_delivs_btn.pack()

    def opn_cases(self):
        rslv_state = "No"
        ViewCases(self.master, self.uid_token, rslv_state)

    def clsd_cases(self):
        rslv_state = "Yes"
        ViewCases(self.master, self.uid_token, rslv_state)


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    InsuranceCompanyView(root, 'insurecomp1')
    root.mainloop()