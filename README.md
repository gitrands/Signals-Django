# Django Signals & Rectangle Class Demo

This Django project demonstrates the default behavior of Django signals regarding execution mode (sync/async), threading, and database transactions. It also includes a custom `Rectangle` class implementation that supports iteration.

## Project Overview
# TO run on local example : /home/jeeva/Documents/accuknox-django/.venv/bin/python manage.py test_signals

The project addresses the following questions with code demonstrations:
1.  **Are Django signals executed synchronously or asynchronously by default?**
2.  **Do Django signals run in the same thread as the caller?**
3.  **Do Django signals run in the same database transaction as the caller?**

Additionally, it implements a `Rectangle` class that yields its length and width when iterated over.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gitrands/Signals-Django.git
    cd Signals-Django
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

## Running the Demo

To see the answers and proofs in action, run the custom management command:

```bash
python manage.py test_signals
```

## What to Expect

The command will output the following sections:

1.  **Question 1: Sync vs Async**
    - Demonstrates that signals are synchronous by introducing a delay in the receiver and measuring the total execution time of the caller.

2.  **Question 2: Threads**
    - Prints the thread name of both the caller and the receiver to prove they run in the same thread.

3.  **Question 3: Transactions**
    - Creates a database entry in a signal receiver while the caller is inside a transaction.
    - Forces a rollback in the caller to demonstrate that the receiver's database operations are also rolled back, proving they share the same transaction.

4.  **Rectangle Class**
    - Iterates over an instance of `Rectangle(10, 5)` and prints the output in the required format:
      ```
      {'length': 10}
      {'width': 5}
      ```

## File Structure

- `signals_app/management/commands/test_signals.py`: Contains the main logic for the signal demonstrations.
- `signals_app/rectangle.py`: Contains the `Rectangle` class implementation.
- `signals_app/models.py`: Contains the `Log` model used for the transaction test.
