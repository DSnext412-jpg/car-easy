here is the way -->Download / Clone Project
Option 1: Using Git
git clone https://github.com/your-username/car-rental-system.git
cd car-rental-system
Option 2: Manual
Download ZIP from GitHub
Extract it
Open folder in VS Code

1. Install Python Dependencies
Open terminal inside project folder and run:
pip install flask mysql-connector-python
Or if you have requirements.txt:
pip install -r requirements.txt

2. Setup MySQL Database
Step 2.1: Open MySQL
Login to MySQL:
mysql -u root -p

Step 2.2: Create Database
CREATE DATABASE car_rental;
USE car_rental;

Step 2.3: Import Tables
If you have database.sql file:
mysql -u root -p car_rental < database.sql

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price INT,
    availability BOOLEAN
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    car_id INT,
    date DATE
);

3. Configure Database in app.py
Open your app.py and update:
mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",   # change this your password
    database="car_rental"
)

4. Run the Flask App
In terminal:
python app.py

5. Open in Browser
Go to:
http://127.0.0.1:5000/

that's it so simple try see keep learning :)
