import tkinter as tk

from data_classes import (
    Conference_system,
    Attendee,
    Ticket,
    ExhibitionPass,
    AllAccessPass,
    Workshop,
    Exhibition
)


class Conference_GUI:
    """
    Main GUI for the GreenWave Conference System.
    Only uses tkinter features from the course:
    Tk, Frame, Label, Entry, Button, pack, grid.
    """

    def __init__(self):
        # create system and load data
        self.system = Conference_system()
        self.system.load_all_data()
        self.system.create_default_exhibition()

        self.current_user = None

        # main window
        self.root = tk.Tk()
        self.root.title("GreenWave Conference System")
        self.root.geometry("700x600")

        # main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20)

        # first screen
        self.show_home_screen()

        # save data when closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    # =======================
    # UTILITIES
    # =======================

    def reset_view(self):
        """Remove all widgets from main_frame."""
        for w in self.main_frame.winfo_children():
            w.destroy()

    def on_close(self):
        """Store all data then close."""
        self.system.store_all_data()
        self.root.destroy()

    # =======================
    # HOME SCREEN
    # =======================

    def show_home_screen(self):
        self.reset_view()
        self.current_user = None

        title = tk.Label(self.main_frame, text="GREENWAVE CONFERENCE",
                         font=("Arial", 16, "bold"))
        title.pack(pady=5)

        subtitle = tk.Label(
            self.main_frame,
            text="April 15–18, 2026  |  Zayed University – AUH Campus"
        )
        subtitle.pack(pady=5)

        sep = tk.Label(self.main_frame, text="=" * 60)
        sep.pack(pady=10)

        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack()

        tk.Button(btn_frame, text="Login", width=20,
                  command=self.display_login).pack(pady=5)

        tk.Button(btn_frame, text="Create Account", width=20,
                  command=self.open_registration_form).pack(pady=5)

        tk.Button(btn_frame, text="Admin Dashboard", width=20,
                  command=self.open_admin_dashboard).pack(pady=5)

    # =======================
    # REGISTRATION
    # =======================

    def open_registration_form(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Create New Account",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        form = tk.Frame(self.main_frame)
        form.pack(pady=10)

        tk.Label(form, text="Full Name:").grid(row=0, column=0, sticky="e", pady=5)
        self.reg_name_entry = tk.Entry(form, width=30)
        self.reg_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Email:").grid(row=1, column=0, sticky="e", pady=5)
        self.reg_email_entry = tk.Entry(form, width=30)
        self.reg_email_entry.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        self.reg_pass_entry = tk.Entry(form, width=30, show="*")
        self.reg_pass_entry.grid(row=2, column=1, pady=5)

        self.reg_msg_label = tk.Label(self.main_frame, text="")
        self.reg_msg_label.pack(pady=5)

        btns = tk.Frame(self.main_frame)
        btns.pack(pady=10)

        tk.Button(btns, text="Create Account", width=15,
                  command=self.save_new_account).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Back", width=15,
                  command=self.show_home_screen).grid(row=0, column=1, padx=5)

    def save_new_account(self):
        name = self.reg_name_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_pass_entry.get()

        if name == "" or email == "" or password == "":
            self.reg_msg_label.config(text="Error: All fields are required")
            return

        if "@" not in email:
            self.reg_msg_label.config(text="Error: Invalid email")
            return

        attendee = Attendee(email, name, password)
        ok = self.system.add_attendee(attendee)

        if ok:
            self.reg_msg_label.config(text="Account created. You can login now.")
            self.reg_name_entry.delete(0, tk.END)
            self.reg_email_entry.delete(0, tk.END)
            self.reg_pass_entry.delete(0, tk.END)
        else:
            self.reg_msg_label.config(text="Error: Email already exists")

    # =======================
    # LOGIN
    # =======================

    def display_login(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Login",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        form = tk.Frame(self.main_frame)
        form.pack(pady=10)

        tk.Label(form, text="Email:").grid(row=0, column=0, sticky="e", pady=5)
        self.login_email_entry = tk.Entry(form, width=30)
        self.login_email_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        self.login_pass_entry = tk.Entry(form, width=30, show="*")
        self.login_pass_entry.grid(row=1, column=1, pady=5)

        self.login_msg_label = tk.Label(self.main_frame, text="")
        self.login_msg_label.pack(pady=5)

        btns = tk.Frame(self.main_frame)
        btns.pack(pady=10)

        tk.Button(btns, text="Login", width=15,
                  command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Back", width=15,
                  command=self.show_home_screen).grid(row=0, column=1, padx=5)

    def login(self):
        email = self.login_email_entry.get()
        password = self.login_pass_entry.get()

        if email == "" or password == "":
            self.login_msg_label.config(text="Error: Enter email and password")
            return

        attendee = self.system.lookup_attendee(email)
        if attendee is None:
            self.login_msg_label.config(text="Error: Email not found")
            return

        if not attendee.verify_password(password):
            self.login_msg_label.config(text="Error: Wrong password")
            return

        self.current_user = attendee
        self.open_attendee_dashboard()

    # =======================
    # ATTENDEE DASHBOARD
    # =======================

    def open_attendee_dashboard(self):
        self.reset_view()

        title = tk.Label(
            self.main_frame,
            text="Welcome, " + self.current_user.full_name + "!",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)

        frame = tk.Frame(self.main_frame)
        frame.pack(pady=10)

        tk.Label(frame, text="--- Purchase Tickets ---").pack(pady=5)
        tk.Button(frame, text="Buy Exhibition Pass", width=25,
                  command=self.start_exhibition_pass_flow).pack(pady=3)
        tk.Button(frame, text="Buy All-Access Pass (500 AED)", width=25,
                  command=self.start_all_access_flow).pack(pady=3)

        tk.Label(frame, text="--- Workshops ---").pack(pady=5)
        tk.Button(frame, text="Book a Workshop", width=25,
                  command=self.book_workshop).pack(pady=3)

        tk.Label(frame, text="--- My Account ---").pack(pady=5)
        tk.Button(frame, text="View My Profile", width=25,
                  command=self.show_user_profile).pack(pady=3)

        tk.Button(frame, text="Logout", width=25,
                  command=self.show_home_screen).pack(pady=20)

    # =======================
    # EXHIBITION PASS
    # =======================

    def start_exhibition_pass_flow(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Buy Exhibition Pass",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        info = tk.Label(self.main_frame, text="Price: 50 AED per exhibition")
        info.pack(pady=5)

        instruct = tk.Label(self.main_frame,
                            text="Enter 1, 2, or 3 (e.g., 1,2) to select exhibitions:")
        instruct.pack(pady=5)

        form = tk.Frame(self.main_frame)
        form.pack(pady=10)

        row = 0
        for ex in self.system.exhibition_list:
            tk.Label(form, text=str(row + 1) + ". " + ex.title).grid(
                row=row, column=0, sticky="w", pady=2)
            row += 1

        tk.Label(form, text="Your selection:").grid(row=row, column=0, sticky="e", pady=10)
        self.ex_select_entry = tk.Entry(form, width=20)
        self.ex_select_entry.grid(row=row, column=1, pady=10)

        row += 1
        tk.Label(form, text="Payment (credit/debit):").grid(row=row, column=0,
                                                             sticky="e", pady=5)
        self.ex_pay_entry = tk.Entry(form, width=20)
        self.ex_pay_entry.grid(row=row, column=1, pady=5)

        self.ex_msg_label = tk.Label(self.main_frame, text="")
        self.ex_msg_label.pack(pady=5)

        btns = tk.Frame(self.main_frame)
        btns.pack(pady=10)

        tk.Button(btns, text="Purchase", width=15,
                  command=self.finalize_ex_pass).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Back", width=15,
                  command=self.open_attendee_dashboard).grid(row=0, column=1, padx=5)

    def finalize_ex_pass(self):
        selection = self.ex_select_entry.get()
        payment = self.ex_pay_entry.get()

        if selection == "":
            self.ex_msg_label.config(text="Error: Select exhibitions")
            return
        if payment == "":
            self.ex_msg_label.config(text="Error: Enter payment method")
            return

        try:
            choices = selection.split(",")
            exhibition_titles = []
            workshop_titles = []

            for choice in choices:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(self.system.exhibition_list):
                    ex = self.system.exhibition_list[idx]
                    exhibition_titles.append(ex.title)
                    for ws in ex.workshop_list:
                        workshop_titles.append(ws.title)

            if len(exhibition_titles) == 0:
                self.ex_msg_label.config(text="Error: Invalid selection")
                return

            ticket = self.system.issue_exhibition_pass(
                self.current_user, exhibition_titles, workshop_titles
            )
            self.ex_msg_label.config(
                text=f"Success! Ticket ID: {ticket.id_code} | Cost: {ticket.cost} AED"
            )
        except:
            self.ex_msg_label.config(text="Error: Invalid input format")

    # =======================
    # ALL-ACCESS PASS
    # =======================

    def start_all_access_flow(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="All-Access Pass",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        info_frame = tk.Frame(self.main_frame)
        info_frame.pack(pady=10)

        tk.Label(info_frame, text="Price: 500 AED", font=("Arial", 12)).pack(pady=5)
        tk.Label(info_frame,
                 text="Includes access to all exhibitions and workshops").pack(pady=5)

        for ex in self.system.exhibition_list:
            tk.Label(info_frame, text="  - " + ex.title).pack(anchor="w")

        form = tk.Frame(self.main_frame)
        form.pack(pady=10)

        tk.Label(form, text="Payment (credit/debit):").grid(row=0, column=0, pady=5)
        self.all_pay_entry = tk.Entry(form, width=20)
        self.all_pay_entry.grid(row=0, column=1, pady=5)

        self.all_msg_label = tk.Label(self.main_frame, text="")
        self.all_msg_label.pack(pady=5)

        btns = tk.Frame(self.main_frame)
        btns.pack(pady=10)

        tk.Button(btns, text="Purchase (500 AED)", width=20,
                  command=self.complete_all_access).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Back", width=15,
                  command=self.open_attendee_dashboard).grid(row=0, column=1, padx=5)

    def complete_all_access(self):
        payment = self.all_pay_entry.get()
        if payment == "":
            self.all_msg_label.config(text="Error: Enter payment method")
            return

        ticket = self.system.issue_all_access_pass(self.current_user)
        self.all_msg_label.config(
            text=f"Success! Ticket ID: {ticket.id_code} | Cost: 500 AED"
        )

    # =======================
    # WORKSHOP BOOKING
    # =======================

    def book_workshop(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Book a Workshop",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        if len(self.current_user.owned_tickets) == 0:
            tk.Label(self.main_frame,
                     text="You need to purchase a ticket first").pack(pady=10)
            tk.Button(self.main_frame, text="Back", width=15,
                      command=self.open_attendee_dashboard).pack(pady=10)
            return

        list_frame = tk.Frame(self.main_frame)
        list_frame.pack(pady=10)

        self.workshop_list = []
        row = 0
        num = 1

        for ex in self.system.exhibition_list:
            tk.Label(list_frame, text="--- " + ex.title + " ---",
                     font=("Arial", 10, "bold")).grid(
                row=row, column=0, sticky="w", pady=5
            )
            row += 1

            for ws in ex.workshop_list:
                self.workshop_list.append(ws)

                can_access = self.current_user.can_book_workshop(ws.title)
                already = ws.title in self.current_user.booked_workshops
                full = ws.is_full()

                if already:
                    status = "[BOOKED]"
                elif full:
                    status = "[FULL]"
                elif not can_access:
                    status = "[NO ACCESS]"
                else:
                    status = "[Available: " + str(ws.get_available_spots()) + "]"

                text = f"{num}. {ws.title} | {ws.schedule} {status}"
                tk.Label(list_frame, text=text).grid(
                    row=row, column=0, sticky="w", pady=1
                )
                row += 1
                num += 1

        select_frame = tk.Frame(self.main_frame)
        select_frame.pack(pady=10)

        tk.Label(select_frame, text="Enter workshop number:").grid(
            row=0, column=0, pady=5
        )
        self.ws_select_entry = tk.Entry(select_frame, width=10)
        self.ws_select_entry.grid(row=0, column=1, pady=5)

        self.ws_msg_label = tk.Label(self.main_frame, text="")
        self.ws_msg_label.pack(pady=5)

        btns = tk.Frame(self.main_frame)
        btns.pack(pady=10)

        tk.Button(btns, text="Book", width=15,
                  command=self.confirm_booking).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Back", width=15,
                  command=self.open_attendee_dashboard).grid(row=0, column=1, padx=5)

    def confirm_booking(self):
        selection = self.ws_select_entry.get()
        if selection == "":
            self.ws_msg_label.config(text="Error: Enter a number")
            return

        try:
            idx = int(selection) - 1
            if idx < 0 or idx >= len(self.workshop_list):
                self.ws_msg_label.config(text="Error: Invalid number")
                return

            workshop = self.workshop_list[idx]
            ok, msg = self.system.process_workshop_reservation(
                self.current_user, workshop.title
            )

            if ok:
                self.ws_msg_label.config(text="Success: " + msg)
                self.book_workshop()
            else:
                self.ws_msg_label.config(text="Error: " + msg)
        except:
            self.ws_msg_label.config(text="Error: Invalid input")

    # =======================
    # PROFILE
    # =======================

    def show_user_profile(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="My Profile",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        info = tk.Frame(self.main_frame)
        info.pack(pady=10)

        tk.Label(info, text="Name: " + self.current_user.full_name).pack(anchor="w")
        tk.Label(info, text="Email: " + self.current_user.email).pack(anchor="w")

        tk.Label(self.main_frame, text="--- My Tickets ---",
                 font=("Arial", 10, "bold")).pack(pady=10)

        if len(self.current_user.owned_tickets) == 0:
            tk.Label(self.main_frame, text="No tickets yet").pack()
        else:
            for t in self.current_user.owned_tickets:
                text = f"{t.id_code} | {t.category} | {t.cost} AED"
                tk.Label(self.main_frame, text=text).pack()

        tk.Label(self.main_frame, text="--- My Workshop Bookings ---",
                 font=("Arial", 10, "bold")).pack(pady=10)

        if len(self.current_user.booked_workshops) == 0:
            tk.Label(self.main_frame, text="No workshops booked").pack()
        else:
            for ws_title in self.current_user.booked_workshops:
                tk.Label(self.main_frame, text="- " + ws_title).pack(anchor="w")

        tk.Button(self.main_frame, text="Back", width=15,
                  command=self.open_attendee_dashboard).pack(pady=20)

    # =======================
    # ADMIN DASHBOARD
    # =======================

    def open_admin_dashboard(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Admin Dashboard",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(self.main_frame)
        frame.pack(pady=10)

        tk.Button(frame, text="View Sales Report", width=25,
                  command=self.view_sales_data).pack(pady=5)
        tk.Button(frame, text="View All Attendees", width=25,
                  command=self.show_all_attendees).pack(pady=5)
        tk.Button(frame, text="Workshop Capacity", width=25,
                  command=self.show_workshop_capacity).pack(pady=5)
        tk.Button(frame, text="Ticket Upgrades", width=25,
                  command=self.open_upgrade_option).pack(pady=5)

        tk.Button(frame, text="Back to Home", width=25,
                  command=self.show_home_screen).pack(pady=20)

    def view_sales_data(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Daily Sales Report",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        report = self.system.daily_sales_report()
        lines = report.split("\n")
        for line in lines:
            tk.Label(self.main_frame, text=line, font=("Courier", 10)).pack(anchor="w")

        tk.Button(self.main_frame, text="Back", width=15,
                  command=self.open_admin_dashboard).pack(pady=20)

    def show_all_attendees(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="All Attendees",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        if len(self.system.attendee_list) == 0:
            tk.Label(self.main_frame, text="No attendees registered yet").pack(pady=10)
        else:
            tk.Label(self.main_frame, text="Name | Email | Tickets",
                     font=("Arial", 10, "bold")).pack(pady=5)
            tk.Label(self.main_frame, text="-" * 50).pack()

            for att in self.system.attendee_list:
                text = f"{att.full_name} | {att.email} | {len(att.owned_tickets)}"
                tk.Label(self.main_frame, text=text).pack(anchor="w")

        tk.Button(self.main_frame, text="Back", width=15,
                  command=self.open_admin_dashboard).pack(pady=20)

    def show_workshop_capacity(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Workshop Capacity Monitor",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        for ex in self.system.exhibition_list:
            tk.Label(self.main_frame, text="--- " + ex.title + " ---",
                     font=("Arial", 10, "bold")).pack(pady=5, anchor="w")

            for ws in ex.workshop_list:
                reg = len(ws.registered_attendees)
                cap = ws.max_capacity
                status = "FULL" if ws.is_full() else "Available"
                text = f"  {ws.title} | {reg}/{cap} | {status}"
                tk.Label(self.main_frame, text=text).pack(anchor="w")

        tk.Button(self.main_frame, text="Back", width=15,
                  command=self.open_admin_dashboard).pack(pady=20)

    def open_upgrade_option(self):
        self.reset_view()

        title = tk.Label(self.main_frame, text="Ticket Upgrades",
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)

        self.upgradeable = []

        for att in self.system.attendee_list:
            for t in att.owned_tickets:
                if t.category != "All-Access Pass":
                    self.upgradeable.append((att, t))

        if len(self.upgradeable) == 0:
            tk.Label(self.main_frame, text="No Exhibition Passes to upgrade").pack(pady=10)
        else:
            list_frame = tk.Frame(self.main_frame)
            list_frame.pack(pady=10)

            num = 1
            for att, ticket in self.upgradeable:
                text = f"{num}. {att.email} | {ticket.id_code} | {ticket.category}"
                tk.Label(list_frame, text=text).pack(anchor="w")
                num += 1

            select_frame = tk.Frame(self.main_frame)
            select_frame.pack(pady=10)

            tk.Label(select_frame, text="Ticket number:").grid(row=0, column=0, pady=5)
            self.upgrade_ticket_entry = tk.Entry(select_frame, width=10)
            self.upgrade_ticket_entry.grid(row=0, column=1, pady=5)

            tk.Label(select_frame, text="Exhibition to add (1/2/3):").grid(row=1, column=0, pady=5)
            self.upgrade_ex_entry = tk.Entry(select_frame, width=10)
            self.upgrade_ex_entry.grid(row=1, column=1, pady=5)

            tk.Label(self.main_frame, text="Exhibitions:").pack()
            for i, ex in enumerate(self.system.exhibition_list):
                text = f"{i + 1}. {ex.title}"
                tk.Label(self.main_frame, text=text).pack(anchor="w")

            tk.Button(self.main_frame, text="Apply Upgrade", width=15,
                      command=self.apply_ticket_upgrade).pack(pady=10)

        self.upgrade_msg_label = tk.Label(self.main_frame, text="")
        self.upgrade_msg_label.pack(pady=5)

        tk.Button(self.main_frame, text="Back", width=15,
                  command=self.open_admin_dashboard).pack(pady=10)

    def apply_ticket_upgrade(self):
        ticket_num = self.upgrade_ticket_entry.get()
        ex_num = self.upgrade_ex_entry.get()

        if ticket_num == "" or ex_num == "":
            self.upgrade_msg_label.config(text="Error: Fill all fields")
            return

        try:
            t_idx = int(ticket_num) - 1
            e_idx = int(ex_num) - 1

            if t_idx < 0 or t_idx >= len(self.upgradeable):
                self.upgrade_msg_label.config(text="Error: Invalid ticket number")
                return
            if e_idx < 0 or e_idx >= len(self.system.exhibition_list):
                self.upgrade_msg_label.config(text="Error: Invalid exhibition number")
                return

            att, ticket = self.upgradeable[t_idx]
            ex = self.system.exhibition_list[e_idx]

            ok, msg = self.system.perform_ticket_upgrade(att, ticket, ex.title)
            if ok:
                self.upgrade_msg_label.config(text="Success: " + msg)
            else:
                self.upgrade_msg_label.config(text="Error: " + msg)
        except:
            self.upgrade_msg_label.config(text="Error: Invalid input")


# =======================
# RUN APP
# =======================

if __name__ == "__main__":
    app = Conference_GUI()