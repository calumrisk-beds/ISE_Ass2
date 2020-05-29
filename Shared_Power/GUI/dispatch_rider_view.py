from tkinter import *
from Shared_Power.GUI.my_bookings import MyBookings
from Shared_Power.GUI.available_deliveries import AvailableDeliveries
from Shared_Power.GUI.my_invoices import MyInvoices


class DispatchRiderView:
    """Dispatch Rider view after logging in.
        Tk() is passed into master from previous class, allowing main Tkinter window to run.
        The user's ID is passed into uid_token."""

    def __init__(self, master, uid_token):
        self.master = master
        self.uid_token = uid_token

        # Main window is retitled
        self.master.title("Dispatch Rider")

        # Frame is packed into main window
        self.frame = Frame(self.master)
        self.frame.pack()

        # Buttons available to user

        self.avai_delivs_btn = Button(self.frame, text="Available Deliveries", command=self.available_delivs)
        self.avai_delivs_btn.pack()

        self.my_delivs_btn = Button(self.frame, text="My Deliveries", command=self.my_delivs)
        self.my_delivs_btn.pack()

        self.my_inv_btn = Button(self.frame, text="My Invoices", command=self.my_inv)
        self.my_inv_btn.pack()

    def available_delivs(self):
        """Called when the available deliveries button is selected."""
        # Calls AvailableDeliveries and passes in the User ID
        AvailableDeliveries(self.master, self.uid_token)

    def my_delivs(self):
        """Called when the my deliveries button is selected."""
        # Calls MyBookings class and passes in the User ID
        # A blank value is passed into Selected Tool because it is not required for this user
        MyBookings(self.master, self.uid_token, '')

    def my_inv(self):
        """Called when the my invoices button is selected."""
        # Calls MyInvoices class and passes in the User ID
        MyInvoices(self.master, self.uid_token)


# For testing purposes
if __name__ == "__main__":
    root = Tk()
    DispatchRiderView(root, 'dr1')
    root.mainloop()
