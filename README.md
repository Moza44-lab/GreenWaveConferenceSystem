Final Assignment 

ICS220 > 21423 Program. Fund.

Professor Areej  Abdulfattah

Ayesha Alzaabi - 202319474

Moza Aldhuhoori - 202307400

Khadeeja Alghafri - 202304750

Due date:  28- Nov - 25 
-----------------------------------

Uml Class Diagram and Description:

<img width="1994" height="1204" alt="image" src="https://github.com/user-attachments/assets/7685e0e4-f9da-4fef-a1b1-d85f6c06b52a" />
https://drive.google.com/file/d/1uR7IzZQxJ7vJ8YFJVIcrOj1ZCciXD7Tj/view?usp=sharing 


The description and the relationship : 

Conference_GUI 
The Conference_GUI class is responsible for showing all the screens of the system using tkinter, including the main page, attendee pages, and admin options. Users interact with these screens to create accounts, log in, buy tickets, book workshops, and upgrade passes. Admins can view sales and confirm upgrades. The GUI does not perform any real processing; instead, it invokes (uses) the Conference_system class to carry out all actions whenever the user clicks a button. This creates a direct association from Conference_GUI to Conference_system


Conference_system 
The Conference_system class manages all the logic and data of the conference. It stores the lists of attendees and exhibitions, loads and saves data, creates default exhibitions, issues tickets, handles workshop reservations, and performs upgrades. It is the main backend used by the GUI. Conference_system has aggregation relationships with both Attendee and Exhibition, shown by white diamonds, because it manages them but they can still exist on their own. It also participates in associations with the GUI since the GUI calls its methods.

Attendee
The Attendee class represents a user who participates in the conference. It stores basic information like the attendee's name and email, along with the list of tickets they own and the workshops they have booked. Attendees can update reservations and manage their tickets. In the UML, an attendee owns one or more Ticket objects through a composition relationship (black diamond), meaning the tickets belong to that attendee. The Attendee class also has an association with Workshop (labeled “attends”), because one attendee may attend many workshops, and each workshop may have many attendees.

Ticket
The Ticket class is a general ticket type that contains common details such as ticket ID, cost, category, allowed workshops, and current bookings. It has basic methods to remove workshops or reservations from the ticket. The Ticket is connected to the Attendee through a composition relationship, because each ticket is owned by one attendee. Ticket also acts as a parent class for the ExhibitionPass and AllAccessPass classes, shown by an inheritance (generalization) relationship.

ExhibitionPass
The ExhibitionPass class is a specific type of ticket that gives access only to selected exhibitions. It inherits from the Ticket class, meaning it uses the base ticket attributes and methods but limits the allowed workshops based on chosen exhibitions. This is shown in the UML as an inheritance arrow from ExhibitionPass to Ticket.



AllAccessPass
 The AllAccessPass class is another specialized ticket that grants access to every workshop and exhibition. Like ExhibitionPass, it extends the Ticket class through an inheritance relationship. It represents the highest level of access in the system and is connected to Ticket through a generalization arrow.




Workshop 
In the UML, Workshop has a many-to-many association with Attendee (labeled “attends”), since many attendees can attend many workshops. It is also connected to Exhibition through an aggregation relationship (white diamond), which means workshops are grouped under an exhibition, but they are not fully owned by it.



Exhibition 
In the UML, Exhibition has an aggregation relationship with Workshop (shown with a white diamond and the label “holds”). This means an exhibition collects or groups workshops together, but the workshops do not depend on the exhibition for their existence. It also has an aggregation relationship with Conference_system.


System Screenshots & Demonstration:
1. Home Page (Main Menu)
<img width="1356" height="854" alt="image" src="https://github.com/user-attachments/assets/ad042d28-80c9-4d2e-9a93-4d17f2b74f0d" />
This screen shows the main interface of the GreenWave Conference System. Users can log in, create an account, or access the admin dashboard.

2. Create Account Screen
<img width="976" height="548" alt="image" src="https://github.com/user-attachments/assets/114e2fe6-75ef-481b-b205-b0e3e5abcc99" />

This screen allows new attendees to register by entering their full name, email, and password.

3. Login Screen
<img width="1248" height="576" alt="image" src="https://github.com/user-attachments/assets/30c2f262-2f5b-4ff6-be53-a18c8924e564" />

This screen verifies attendee credentials. If the email does not exist, the system shows an error message such as “Email not found.”

4. User Dashboard (After Login)
<img width="886" height="590" alt="image" src="https://github.com/user-attachments/assets/f9cae541-9824-47c2-88c7-2dfe5b0ad607" />

This screen is shown after a successful login. The attendee can buy tickets, book workshops, check their profile, or log out.

5. Buy All-Access Pass
<img width="930" height="606" alt="image" src="https://github.com/user-attachments/assets/8f148599-b796-41ba-a225-7d0d3665f7b6" />


This screen allows the user to purchase the All-Access Pass. It includes all exhibitions and workshops for a fixed price.

6. Buy Exhibition Pass
<img width="954" height="740" alt="image" src="https://github.com/user-attachments/assets/ea5b5fb9-5b3e-4d5d-bbeb-63a5ec68faad" />

This screen allows selecting 1, 2, or 3 exhibitions for 50 AED each. A success message appears with the ticket ID after payment.

7. Book a Workshop
<img width="780" height="690" alt="image" src="https://github.com/user-attachments/assets/430f87b4-ae8d-47bf-9c80-892e7a518e82" />


This screen displays all workshops, grouped by exhibition, along with their availability. The user enters the workshop number to book it.

8. Profile Page
<img width="970" height="688" alt="image" src="https://github.com/user-attachments/assets/5a093523-0c4c-4d75-9429-08c622265a67" />

This page shows the attendee’s information, purchased tickets, and workshop bookings.

9. Admin Dashboard

<img width="970" height="688" alt="image" src="https://github.com/user-attachments/assets/b9d61f5b-916f-414f-9760-29d212aa677c" />

This screen allows the admin to view all attendees, workshop capacities, and process ticket upgrades.

10. All Attendees List (Admin)
<img width="856" height="634" alt="image" src="https://github.com/user-attachments/assets/27af52fb-6757-419a-b658-8e53860a7c71" />


This page displays all registered users, their emails, and how many tickets each one has.

11. Workshop Capacity Monitor (Admin)
<img width="742" height="628" alt="image" src="https://github.com/user-attachments/assets/bcdcd665-a603-4351-a7e7-d1899802decd" />

This page shows the number of bookings for each workshop and the remaining available spots.

12. Ticket Upgrade Page
<img width="1024" height="864" alt="image" src="https://github.com/user-attachments/assets/938a9f4d-4b50-4ba5-887e-830bc5bee7d1" />

This screen allows the admin to upgrade an attendee’s exhibition pass by entering:
- Ticket number
- Exhibition to add
 A success confirmation appears after upgrade.


13. Daily Sales Report
<img width="814" height="602" alt="image" src="https://github.com/user-attachments/assets/874df491-0756-460d-b826-194889ee00a3" />

Lists each date and the total AED amount collected from ticket sales.

14. Error Handling Example
<img width="1050" height="680" alt="image" src="https://github.com/user-attachments/assets/a58a3fb5-25ca-4f5b-a827-eb4e858e2eb1" />

This screenshot demonstrates how the system handles incorrect login attempts with an error message.






