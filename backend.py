import mysql.connector
from mysql.connector import Error

class RailwayBackend:
    def __init__(self):
        # --- CONFIGURATION ---
        # CHANGE THESE CREDENTIALS to match your MySQL installation
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Pradeep@2005',  # <--- PUT YOUR REAL MYSQL PASSWORD HERE
            'database': 'railway_system'
        }
        self.init_database()

    def get_connection(self):
        """Creates a new database connection."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def init_database(self):
        """Automatically creates the database and tables if they don't exist."""
        try:
            # 1. Connect to Server to check/create Database
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            conn.close()

            # 2. Connect to the specific Database to create Tables
            conn = self.get_connection()
            cursor = conn.cursor()

            # Table: Users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100),
                    email VARCHAR(100),
                    age INT,
                    aadhar VARCHAR(20),
                    username VARCHAR(50) UNIQUE,
                    password VARCHAR(255),
                    role VARCHAR(10) DEFAULT 'passenger'
                )
            """)

            # Table: Trains
            # IMPORTANT: Added date, total_seats, price, delay columns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trains (
                    train_id INT AUTO_INCREMENT PRIMARY KEY,
                    number VARCHAR(20) UNIQUE,
                    name VARCHAR(100),
                    source VARCHAR(50),
                    dest VARCHAR(50),
                    date DATE,
                    time VARCHAR(20),
                    seats INT,
                    total_seats INT,
                    price FLOAT DEFAULT 0.0,
                    delay INT DEFAULT 0,
                    status VARCHAR(20) DEFAULT 'On Time'
                )
            """)

            # Table: Bookings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INT AUTO_INCREMENT PRIMARY KEY,
                    pnr VARCHAR(20) UNIQUE,
                    user_id INT,
                    train_id INT,
                    booking_date DATE,
                    seat_number INT,
                    status VARCHAR(20) DEFAULT 'Confirmed',
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (train_id) REFERENCES trains(train_id) ON DELETE CASCADE
                )
            """)
            
            # Create Default Admin if not exists
            cursor.execute("SELECT * FROM users WHERE username = 'Admin'")
            if not cursor.fetchone():
                cursor.execute("INSERT INTO users (full_name, username, password, role) VALUES ('System Admin', 'Admin', '12345', 'admin')")
            
            conn.commit()
            print("Database initialized successfully.")
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Database Init Error: {e}")

    # --- DATA METHODS ---

    def register_user(self, data):
        conn = self.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (full_name, email, age, aadhar, username, password, role) VALUES (%s, %s, %s, %s, %s, %s, 'passenger')"
            values = (data['name'], data['email'], data['age'], data['aadhar'], data['username'], data['password'])
            cursor.execute(query, values)
            conn.commit()
            return True
        except Error as e:
            print(f"Register Error: {e}")
            return False
        finally:
            conn.close()

    def login_user(self, username, password, role_check):
        # HARDCODED ADMIN CHECK (Bypasses Database for this specific user)
        if role_check == 'admin' and username == 'Admin' and password == '12345':
            return {'user_id': 0, 'username': 'Admin', 'full_name': 'System Administrator', 'role': 'admin'}

        conn = self.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                if role_check and user['role'] != role_check:
                    return None
                return user
            return None
        finally:
            conn.close()

    def get_all_users(self):
        conn = self.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT full_name as name, username, email, role FROM users")
            return cursor.fetchall()
        finally:
            conn.close()

    def add_train(self, data):
        conn = self.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            
            # Handle date: If empty string is sent, store None (NULL)
            journey_date = data.get('date')
            if journey_date == '':
                journey_date = None

            query = "INSERT INTO trains (number, name, source, dest, date, time, seats, total_seats, price, delay, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            values = (
                data['number'], 
                data['name'], 
                data['source'], 
                data['dest'], 
                journey_date, 
                data['time'], 
                data['seats'], 
                data['seats'], # Total seats same as current seats initially
                data.get('price', 0), 
                data.get('delay', 0), 
                data.get('status', 'On Time')
            )
            cursor.execute(query, values)
            conn.commit()
            return True
        except Error as e:
            print(f"Add Train Error: {e}")
            return False
        finally:
            conn.close()

    def delete_train(self, train_id):
        conn = self.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM trains WHERE train_id = %s"
            cursor.execute(query, (train_id,))
            conn.commit()
            return True
        except Error as e:
            print(f"Delete Train Error: {e}")
            return False
        finally:
            conn.close()

    def get_all_trains(self):
        conn = self.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            # Fix: Ensure date is formatted as string for JSON serialization
            cursor.execute("SELECT *, DATE_FORMAT(date, '%Y-%m-%d') as date FROM trains")
            return cursor.fetchall()
        finally:
            conn.close()

    def book_ticket(self, data):
        conn = self.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            # 1. Check availability
            cursor.execute("SELECT seats FROM trains WHERE train_id = %s", (data['trainId'],))
            result = cursor.fetchone()
            
            if result and result[0] > 0:
                # 2. Insert Booking
                query = "INSERT INTO bookings (pnr, user_id, train_id, booking_date, seat_number) VALUES (%s, %s, %s, %s, %s)"
                values = (data['pnr'], data['userId'], data['trainId'], data['date'], data['seat'])
                cursor.execute(query, values)
                
                # 3. Decrement Seat Count
                cursor.execute("UPDATE trains SET seats = seats - 1 WHERE train_id = %s", (data['trainId'],))
                conn.commit()
                return True
            return False
        except Error as e:
            print(f"Booking Error: {e}")
            return False
        finally:
            conn.close()

    def get_user_bookings(self, user_id):
        conn = self.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT b.pnr, DATE_FORMAT(b.booking_date, '%Y-%m-%d') as booking_date, b.seat_number, t.name as train_name, t.number as train_number, t.source, t.dest 
                FROM bookings b
                JOIN trains t ON b.train_id = t.train_id
                WHERE b.user_id = %s
                ORDER BY b.booking_id DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def get_booking_by_pnr(self, pnr):
        conn = self.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT b.pnr, b.status, b.seat_number, t.name as train_name, t.number as train_number 
                FROM bookings b
                JOIN trains t ON b.train_id = t.train_id
                WHERE b.pnr = %s
            """
            cursor.execute(query, (pnr,))
            return cursor.fetchone()
        finally:
            conn.close()