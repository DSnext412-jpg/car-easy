from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '----' 
app.config['MYSQL_DB'] = 'car_rental_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.secret_key = 'your_secret_key'

mysql = MySQL(app)


@app.route('/')
def home():
    booking_summary = None
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("""
            select b.pickup_date, b.return_date, b.total_price, c.name AS car_name
            from bookings b
            join cars c ON b.car_id = c.id
            where b.user_id = %s
            order by b.pickup_date DESC
            LIMIT 5
        """, (session['user_id'],))
        booking_summary = cur.fetchall()
        cur.close()

    return render_template('home.html', booking_summary=booking_summary)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'] 

        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "insert into users (name, email, password) values (%s, %s, %s)",
                (name, email, password)
            )
            mysql.connection.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Email already registered.', 'danger')
        finally:
            cur.close()

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/cars')
def cars():
    cur = mysql.connection.cursor()
    cur.execute("select * from cars")
    cars_data = cur.fetchall()
    cur.close()
    return render_template('cars.html', cars=cars_data)


@app.route('/car/<int:car_id>')
def car_details(car_id):
    cur = mysql.connection.cursor()
    cur.execute("select * from cars where id = %s", (car_id,))
    car = cur.fetchone()
    cur.close()

    reviews = [
        {'author': 'Dipak sonawane', 'rating': 5, 'comment': 'Excellent car!'},
        {'author': 'vishal patil', 'rating': 4, 'comment': 'Good experience'}
    ]

    return render_template('car_details.html', car=car, reviews=reviews)


@app.route('/book/<int:car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if 'user_id' not in session:
        flash('Login required to book a car.', 'warning')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("select * from cars where id = %s", (car_id,))
    car = cur.fetchone()

    if request.method == 'POST':
        pickup_date = datetime.strptime(request.form['pickup_date'], '%Y-%m-%d')
        return_date = datetime.strptime(request.form['return_date'], '%Y-%m-%d')

        if pickup_date >= return_date:
            flash('Return date must be after pickup date.', 'danger')
        else:
            days = (return_date - pickup_date).days
            total_price = days * car['price_per_day']

            try:
                cur.execute("""
                    insert into bookings (user_id, car_id, pickup_date, return_date, total_price)
                    values (%s, %s, %s, %s, %s)
                """, (session['user_id'], car_id, pickup_date, return_date, total_price))
                mysql.connection.commit()
                flash('Booking successful!', 'success')
                return redirect(url_for('dashboard'))
            except Exception:
                flash('Booking failed.', 'danger')

    cur.close()
    return render_template('booking.html', car=car)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Login required.', 'warning')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        select b.pickup_date, b.return_date, b.total_price, c.name AS car_name
        from bookings b
        join cars c ON b.car_id = c.id
        where b.user_id = %s
    """, (session['user_id'],))
    bookings = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True)
