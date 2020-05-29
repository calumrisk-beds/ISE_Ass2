from tkinter import *
from Shared_Power.GUI.create_tool import CreateTool
from Shared_Power.GUI.my_tools import MyTools
from Shared_Power.GUI.my_invoices import MyInvoices


class ToolOwnerView:
    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        self.master.title("Tool Owner")

        self.frame = Frame(self.master)
        self.frame.pack()

        self.add_tl_btn = Button(self.frame, text="Add Tool", command=self.add_tool)
        self.add_tl_btn.pack()

        self.mng_tls_btn = Button(self.frame, text="My Tools", command=self.my_tls)
        self.mng_tls_btn.pack()

        self.my_inv_btn = Button(self.frame, text="My Invoices", command=self.my_inv)
        self.my_inv_btn.pack()

    def add_tool(self):
        CreateTool(self.master, self.uid_token)

    def my_tls(self):
        MyTools(self.master, self.uid_token)

    def my_inv(self):
        MyInvoices(self.master, self.uid_token)


if __name__ == "__main__":
    root = Tk()
    ToolOwnerView(root, 'test4')
    root.mainloop()
