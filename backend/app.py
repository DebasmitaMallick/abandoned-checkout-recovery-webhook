from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
import sqlite3
import datetime
from celery import Celery, Task
from datetime import datetime, timedelta
import smtplib
import pytz
from flask_cors import CORS
import os


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app = Flask(__name__)

CORS(app)

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)
celery_app.conf.timezone = 'UTC'

DATABASE = 'database/abandoned_checkout.db'

# Converting local time to UTC
def local_to_utc(local_dt):
    local_tz = pytz.timezone('Asia/Kolkata')
    local_dt = local_tz.localize(local_dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt

def send_email(receiver_email_id, message_content):
    sender_email_id = os.environ["sender_email_id_webhook"]
    password = os.environ["email_app_password_webhook"]

    message = MIMEMultipart()
    message["From"] = sender_email_id
    message["To"] = receiver_email_id
    message["Subject"] = "Recover Your Abandoned Cart"

    message.attach(MIMEText(message_content, "plain"))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email_id, password)
    s.sendmail(sender_email_id, receiver_email_id, message.as_string())
    s.quit()

@celery_app.task
def send_scheduled_message(checkout_id, message_time):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Checking if the message time has passed
    message_time_utc = local_to_utc(message_time)
    now_utc = local_to_utc(datetime.now())
    if now_utc >= message_time_utc:
        # Retrieving the abandoned checkout details
        cursor.execute('''SELECT cart_token, email, recovery_url FROM abandoned_checkouts WHERE id = ?''', (checkout_id,))
        checkout = cursor.fetchone()

        if checkout:
            cart_token, email, recovery_url = checkout

            # Checking if the user has placed an order
            cursor.execute('''SELECT id FROM orders WHERE cart_token = ?''', (cart_token,))
            order = cursor.fetchone()

            if order:
                print(f"Order already placed for cart_token {cart_token}. Skipping message.")
            else:
                try:
                    print(f"Sending message to {email} to recover cart: {recovery_url}")
                    message = "Please complete your order by visiting this url: "+recovery_url
                    send_email(email, message)
                    cursor.execute('''INSERT INTO scheduled_messages (checkout_id, message, message_time)
                            VALUES (?, ?, ?)''', (checkout_id, message, message_time))
                    conn.commit()
                except Exception as e:
                    print('failed sending email', e)

    conn.close()

@app.route('/abandoned_checkout', methods=['POST'])
def handle_abandoned_checkout():
    data = request.json
    cart_token = data.get('cart_token')
    email = data.get('email')
    recovery_url = data.get('recovery_url')
    customer_id = data.get('customer_id')
    abandonment_time = datetime.now()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Inserting into abandoned_checkouts
    cursor.execute('''INSERT INTO abandoned_checkouts (cart_token, email, abandoned_at, recovery_url, customer_id)
                    VALUES (?, ?, ?, ?, ?)''', 
                (cart_token, email, abandonment_time, recovery_url, customer_id))
    conn.commit()
    checkout_id = cursor.lastrowid
    print('checkout_id', checkout_id)

    schedule = [
        timedelta(seconds=0),
        timedelta(minutes=30),
        timedelta(days=1),
        timedelta(days=3)
    ]

    for offset in schedule:
        message_time = abandonment_time + offset
        message_time_utc = local_to_utc(message_time)
        # Scheduling the messages
        send_scheduled_message.apply_async((checkout_id, message_time), eta=message_time_utc)

    conn.close()

    return jsonify({"status": "Abandoned checkout recorded and messages scheduled"}), 201

@app.route('/complete_order', methods=['POST'])
def complete_order():
    data = request.json
    cart_token = data.get('cart_token')
    created_at = datetime.now()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Inserting completed order record
    cursor.execute('''INSERT INTO orders (cart_token, created_at) 
                      VALUES (?, ?)''', (cart_token, created_at))

    conn.commit()
    conn.close()

    return jsonify({"status": "Order completed"}), 200

@app.route('/messages_and_orders', methods=['GET'])
def get_scheduled_messages():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetching all the messages and order details
    cursor.execute('''
        SELECT 
            sm.id AS message_id,
            sm.message AS message_content,
            sm.message_time AS message_sent_at,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.email,
            c.phone,
            ac.cart_token,
            ac.recovery_url,
            o.id AS order_id,
            o.created_at AS order_created_at
        FROM 
            scheduled_messages sm
        JOIN 
            abandoned_checkouts ac ON sm.checkout_id = ac.id
        JOIN 
            customers c ON ac.customer_id = c.id
        LEFT JOIN 
            orders o ON ac.cart_token = o.cart_token
            AND o.created_at > sm.message_time
            AND NOT EXISTS (
                SELECT 1 FROM scheduled_messages sm2
                WHERE sm2.checkout_id = sm.checkout_id
                AND sm2.message_time > sm.message_time
                AND sm2.message_time < o.created_at
            )
        ORDER BY 
            sm.message_time DESC;
    ''')

    data = cursor.fetchall()

    response = [{"message_id": row[0], "message":row[1],"message_sent_at": row[2], "customer_name": row[3], "email":row[4], "order_id": row[8], "order_created_at": row[9]} for row in data]

    conn.close()

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5002)

