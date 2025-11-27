import pickle
from datetime import date

# =======================
# EXHIBITION CLASS
# =======================

class Exhibition:
    def __init__(self, exhibition_id="", title=""):
        self.exhibition_id = exhibition_id
        self.title = title
        self.workshop_list = []

    def insert_workshop(self, workshop):
        self.workshop_list.append(workshop)

    def delete_workshop(self, workshop):
        if workshop in self.workshop_list:
            self.workshop_list.remove(workshop)

    def __str__(self):
        return self.exhibition_id + "," + self.title + "," + str(len(self.workshop_list)) + " workshops"


# =======================
# WORKSHOP CLASS
# =======================

class Workshop:
    def __init__(self, title="", schedule="", max_capacity=30):
        self.title = title
        self.schedule = schedule
        self.max_capacity = max_capacity
        self.registered_attendees = []

    def register(self, attendee_email):
        if len(self.registered_attendees) >= self.max_capacity:
            return False
        if attendee_email not in self.registered_attendees:
            self.registered_attendees.append(attendee_email)
            return True
        return False

    def unregister(self, attendee_email):
        if attendee_email in self.registered_attendees:
            self.registered_attendees.remove(attendee_email)
            return True
        return False

    def get_available_spots(self):
        return self.max_capacity - len(self.registered_attendees)

    def is_full(self):
        return len(self.registered_attendees) >= self.max_capacity

    def __str__(self):
        return self.title + "," + self.schedule + "," + str(len(self.registered_attendees)) + "/" + str(self.max_capacity)


# =======================
# TICKET CLASS
# =======================

class Ticket:
    def __init__(self, id_code="", cost=0.0, category=""):
        self.id_code = id_code
        self.cost = cost
        self.category = category
        self.allowed_workshops = []
        self.current_bookings = []
        self.purchase_date = ""

    def remove_allowed_workshop(self, workshop_title):
        if workshop_title in self.allowed_workshops:
            self.allowed_workshops.remove(workshop_title)

    def remove_booking(self, workshop_title):
        if workshop_title in self.current_bookings:
            self.current_bookings.remove(workshop_title)
            return True
        return False

    def add_booking(self, workshop_title):
        if workshop_title not in self.current_bookings:
            self.current_bookings.append(workshop_title)

    def can_access_workshop(self, workshop_title):
        return workshop_title in self.allowed_workshops

    def __str__(self):
        return self.id_code + "," + self.category + "," + str(self.cost) + " AED"


# =======================
# EXHIBITION PASS
# =======================

class ExhibitionPass(Ticket):
    def __init__(self, id_code="", exhibitions_list=None):
        Ticket.__init__(self)
        self.id_code = id_code
        self.exhibitions = exhibitions_list if exhibitions_list else []
        self.cost = len(self.exhibitions) * 50.0

        count = len(self.exhibitions)
        if count == 1:
            self.category = "Single Exhibition Pass"
        elif count == 2:
            self.category = "Dual Exhibition Pass"
        else:
            self.category = str(count) + "-Exhibition Pass"

    def add_exhibition(self, exhibition_title, workshops):
        if exhibition_title not in self.exhibitions:
            self.exhibitions.append(exhibition_title)
            for ws in workshops:
                if ws not in self.allowed_workshops:
                    self.allowed_workshops.append(ws)
            self.cost = len(self.exhibitions) * 50.0

    def __str__(self):
        return self.id_code + "," + self.category + "," + str(self.cost) + " AED"


# =======================
# ALL ACCESS PASS
# =======================

class AllAccessPass(Ticket):
    def __init__(self, id_code=""):
        Ticket.__init__(self)
        self.id_code = id_code
        self.cost = 500.0
        self.category = "All-Access Pass"

    def __str__(self):
        return self.id_code + "," + self.category + "," + str(self.cost) + " AED"


# =======================
# ATTENDEE CLASS
# =======================

class Attendee:
    def __init__(self, email="", full_name="", password=""):
        self.email = email
        self.full_name = full_name
        self.password = password
        self.owned_tickets = []
        self.booked_workshops = []

    def assign_ticket(self, ticket):
        self.owned_tickets.append(ticket)

    def add_booking(self, workshop_title):
        if workshop_title not in self.booked_workshops:
            self.booked_workshops.append(workshop_title)
            return True
        return False

    def cancel_booking(self, workshop_title):
        if workshop_title in self.booked_workshops:
            self.booked_workshops.remove(workshop_title)
            return True
        return False

    def can_book_workshop(self, workshop_title):
        for ticket in self.owned_tickets:
            if ticket.can_access_workshop(workshop_title):
                return True
        return False

    def verify_password(self, password):
        return self.password == password

    def __str__(self):
        return self.email + "," + self.full_name + "," + str(len(self.owned_tickets)) + " tickets"


# =======================
# CONFERENCE SYSTEM (WITH PICKLE)
# =======================

class Conference_system:
    def __init__(self):
        self.attendee_list = []
        self.exhibition_list = []
        self.ticket_counter = 0
        self.sales_list = []

    # ------------ PICKLE SAVE/LOAD ------------

    def _save_file(self, filename, data):
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    def _load_file(self, filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except:
            return []

    def load_all_data(self):
        self.attendee_list = self._load_file("attendees.dat")
        self.exhibition_list = self._load_file("exhibitions.dat")
        self.sales_list = self._load_file("sales.dat")
        self.ticket_counter = len(self.sales_list)

    def store_all_data(self):
        self._save_file("attendees.dat", self.attendee_list)
        self._save_file("exhibitions.dat", self.exhibition_list)
        self._save_file("sales.dat", self.sales_list)

    # ------------ DEFAULT EXHIBITIONS ------------

    def create_default_exhibition(self):
        if len(self.exhibition_list) > 0:
            return

        ex1 = Exhibition("EXH1", "Climate Tech Innovations")
        ex1.insert_workshop(Workshop("Solar Futures", "10:00-11:00"))
        ex1.insert_workshop(Workshop("Smart Grids", "11:30-12:30"))
        ex1.insert_workshop(Workshop("Green Mobility", "13:00-14:00"))

        ex2 = Exhibition("EXH2", "Policy & Community Action")
        ex2.insert_workshop(Workshop("Local Policy Labs", "10:00-11:00"))
        ex2.insert_workshop(Workshop("Community Projects", "11:30-12:30"))
        ex2.insert_workshop(Workshop("Youth Climate Leaders", "13:00-14:00"))

        ex3 = Exhibition("EXH3", "Sustainable Lifestyles")
        ex3.insert_workshop(Workshop("Zero Waste Homes", "10:00-11:00"))
        ex3.insert_workshop(Workshop("Green Fashion", "11:30-12:30"))
        ex3.insert_workshop(Workshop("Mindful Consumption", "13:00-14:00"))

        self.exhibition_list = [ex1, ex2, ex3]

    # ------------ ATTENDEE ------------

    def add_attendee(self, attendee):
        for a in self.attendee_list:
            if a.email == attendee.email:
                return False
        self.attendee_list.append(attendee)
        return True

    def lookup_attendee(self, email):
        for a in self.attendee_list:
            if a.email == email:
                return a
        return None

    # ------------ TICKET CREATION ------------

    def _next_ticket_id(self, prefix):
        self.ticket_counter += 1
        return f"{prefix}-{self.ticket_counter:04d}"

    def issue_exhibition_pass(self, attendee, exhibition_titles, workshop_titles):
        ticket_id = self._next_ticket_id("GW-EXH")
        ticket = ExhibitionPass(ticket_id, exhibition_titles)
        ticket.allowed_workshops = workshop_titles
        ticket.purchase_date = date.today().isoformat()
        attendee.assign_ticket(ticket)
        self.sales_list.append((ticket.purchase_date, ticket.category, ticket.cost))
        return ticket

    def issue_all_access_pass(self, attendee):
        ticket_id = self._next_ticket_id("GW-ALL")
        ticket = AllAccessPass(ticket_id)

        for ex in self.exhibition_list:
            for ws in ex.workshop_list:
                if ws.title not in ticket.allowed_workshops:
                    ticket.allowed_workshops.append(ws.title)

        ticket.purchase_date = date.today().isoformat()
        attendee.assign_ticket(ticket)
        self.sales_list.append((ticket.purchase_date, ticket.category, ticket.cost))
        return ticket

    # ------------ WORKSHOP BOOKING ------------

    def _find_workshop(self, title):
        for ex in self.exhibition_list:
            for ws in ex.workshop_list:
                if ws.title == title:
                    return ws
        return None

    def process_workshop_reservation(self, attendee, workshop_title):
        if not attendee.can_book_workshop(workshop_title):
            return False, "Your ticket does not allow this workshop."

        ws = self._find_workshop(workshop_title)
        if ws is None:
            return False, "Workshop not found."

        if ws.is_full():
            return False, "Workshop is already full."

        if workshop_title in attendee.booked_workshops:
            return False, "You already booked this workshop."

        ws.register(attendee.email)
        attendee.add_booking(workshop_title)
        return True, "Workshop booked successfully."

    # ------------ SALES REPORT ------------

    def daily_sales_report(self):
        if len(self.sales_list) == 0:
            return "No sales recorded yet."

        totals = {}
        for d, ttype, amt in self.sales_list:
            totals.setdefault(d, 0)
            totals[d] += amt

        report = "Date       | Amount\n----------------------\n"
        for d in totals:
            report += f"{d} | {totals[d]} AED\n"
        return report

    # ------------ TICKET UPGRADE ------------

    def perform_ticket_upgrade(self, attendee, ticket, exhibition_title):
        if ticket.category == "All-Access Pass":
            return False, "Already Full Access."

        for ex in self.exhibition_list:
            if ex.title == exhibition_title:
                ws_titles = [ws.title for ws in ex.workshop_list]
                ticket.add_exhibition(exhibition_title, ws_titles)
                self.sales_list.append((date.today().isoformat(), "Upgrade", 50.0))
                return True, "Upgrade successful."

        return False, "Exhibition not found."