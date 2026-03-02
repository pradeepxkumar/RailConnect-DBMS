# 🚆 RailConnect  
### A Relational Database Management System for Railway Operations


RailConnect is a web-based Railway Management System developed to understand and implement core **Database Management System (DBMS)** concepts in a practical way.

This project connects a **MySQL relational database** with a **Python Flask backend** and a responsive frontend built using **HTML, Tailwind CSS, and JavaScript**.

The main purpose of this project is to demonstrate how relational databases work in real-world systems like railway reservation platforms.

📄 Full Project Report: [DBMS_Report.pdf](./DBMS_Report.pdf)


# 📌 Project Overview

Railways are one of the most important transportation systems. Managing train schedules, passengers, and seat availability manually can be complex and error-prone.

RailConnect automates:

- Train scheduling  
- Passenger registration  
- Ticket booking  
- Seat management  
- Admin control panel  

This project focuses on implementing:

- Database normalization  
- Primary & Foreign keys  
- Referential integrity  
- ACID properties  
- CRUD operations  
- Full-stack integration  


# 🏗️ System Architecture

RailConnect follows a **Three-Tier Architecture**:

Frontend (HTML, CSS, JavaScript)  
↓  
Backend (Python Flask)  
↓  
Database (MySQL Server 8.0)

### 1️ Presentation Layer (Frontend)
- HTML5  
- Tailwind CSS  
- Vanilla JavaScript  
- Fetch API for backend communication  

### 2️ Application Layer (Backend)
- Python  
- Flask Framework  
- MySQL Connector  
- REST API endpoints  

### 3️ Data Layer (Database)
- MySQL 8.0  
- Normalized relational schema  
- Foreign key constraints  
- ON DELETE CASCADE  


# 🗄️ Database Design

The database is the core of this system.

## Main Entities

### 👤 Users
Stores login credentials and profile information.

### 🚆 Trains
Stores train number, source, destination, seat availability, price, and delay.

### 🎫 Bookings
Links users and trains through foreign keys.


## 🔗 Relationships

- One User → Many Bookings (1:N)
- One Train → Many Bookings (1:N)

Foreign keys ensure:
- No invalid booking can exist
- Data consistency is maintained
- Referential integrity is preserved

`ON DELETE CASCADE` ensures that when a train is deleted, all related bookings are automatically removed.



# ⚙️ Core Functionalities (CRUD Operations)

## ✅ CREATE
- User Registration  
- Add Train (Admin)  
- Book Ticket  

## 📖 READ
- Login Verification  
- View Available Trains  
- View My Bookings (JOIN query used)  

## 🔄 UPDATE
- Automatic seat decrement during booking  
- Delay updates  

## ❌ DELETE
- Admin can delete trains  
- Related bookings auto-delete (CASCADE)  


# 🔌 Backend & Database Connectivity

- Parameterized queries (`%s`) used to prevent SQL injection  
- Each request creates and closes a database connection properly  
- Flask APIs handle JSON data  

### Important API Endpoints

- `/api/register`
- `/api/login`
- `/api/book`

Seat booking is handled carefully to avoid race conditions.


# 🖥️ User Interface

## 🔐 Split-Screen Login

![Login Screen](images/login.png)

- Passenger Login  
- Admin Login  
- Registration Form  
- Responsive layout  


## 👤 Passenger Dashboard

![Passenger Dashboard](images/passenger_dashboard.png)

Features:
- Search by source, destination, date  
- Real-time seat availability  
- Delay indicator  
- PNR tracking  


## 🛠️ Admin Dashboard

![Admin Dashboard](images/admin_dashboard.png)

Features:
- Train statistics  
- Add new train  
- Delete train  
- View seat availability  



# 🔄 End-to-End Workflow

1. User registers  
2. Data is validated  
3. Record inserted into MySQL  
4. User logs in  
5. Searches train  
6. Books ticket  
7. Backend checks seat availability  
8. Seat count is reduced  
9. PNR generated  
10. Admin dashboard reflects changes instantly  


# 📚 Key Learnings

- Importance of Foreign Keys  
- Database normalization  
- Maintaining relational consistency  
- Real-time data updates  
- Frontend–backend synchronization  
- Using SQL JOIN operations  


# 🚧 Challenges Solved

**Problem:** Updating UI without reloading page  

**Solution:** Used JavaScript `fetch()` to dynamically update content using JSON responses from Flask.



# 🚀 Future Scope

- Payment gateway integration  
- Seat selection interface  
- Live train tracking  
- Password hashing  
- JWT authentication  
- Secure session handling  



# 🛠️ Tech Stack

| Layer     | Technology |
|-----------|------------|
| Frontend  | HTML5, Tailwind CSS, JavaScript |
| Backend   | Python, Flask |
| Database  | MySQL 8.0 |


# 📂 Project Structure

RailConnect/
│
├── app.py
├── backend.py
├── templates/
├── static/
├── DBMS_Report.pdf
└── README.md



# 👨‍💻 Contributors

- Pradeep Kumar  
- Harphool Singh Bajdoliya  
- Academic Guidance: Dr. Surya Prakash  


# 🎯 Conclusion

RailConnect demonstrates how a relational database powers a real-world web application.  
It shows practical implementation of DBMS concepts through a complete full-stack project.

This project builds a strong foundation for understanding how modern reservation systems work.
