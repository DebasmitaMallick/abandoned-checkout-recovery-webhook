# Abandoned Checkout Recovery Plugin

This project is an Abandoned Checkout Recovery Plugin for e-commerce businesses. It is designed to help recover potentially lost sales by sending automated recovery messages to customers who have abandoned their checkout process.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Webhook Handling:** Captures checkout abandonment and order placement events via webhooks.
- **Automated Messaging:** Sends customizable, scheduled recovery messages to customers.
- **Order Detection:** Stops sending recovery messages if an order is placed.
- **User Interface:** Displays a table of sent messages and the orders created through these messages.
- **SQLite Database:** Stores customer data, abandoned checkouts, sent messages, and orders.

## Technologies Used

### Backend:
- **Python**
- **Flask**
- **Celery**
- **SQLite**
- **SMTP (for sending emails)**

### Frontend:
- **React.js**
- **Tailwind CSS**

## Installation

### Prerequisites:
- Python 3.x
- Node.js and npm

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/abandoned-checkout-recovery-backend.git
   cd abandoned-checkout-recovery-backend
   ```
2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```
4. **Set up the SQLite database:**

    ```bash
    python setup_db.py  # Or any script that initializes your database schema
    ```
5. **Run the Flask server:**

    ```bash
    python app.py
    ```
6. **Start the Redis server:**

    ```bash
    sudo service redis-server start
    ```
7. **Start the Celery worker:**

    ```bash
    celery -A app.celery_app worker --loglevel=info --pool=solo
    ```