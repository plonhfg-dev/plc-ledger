import json
import random
import os
from datetime import datetime
import http.server
import socketserver

DB_FILE = 'debts.json'

def init_db():
    """Ensures the database file exists right away to prevent HTML 404 errors."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)

def load_db():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_unique_serial(db):
    while True:
        serial = str(random.randint(100000, 999999))
        if serial not in db:
            return serial

def create_debt_record():
    db = load_db()
    print("\n--- Create New Debt Record ---")
    debt_number = input("Enter Debt Number (e.g., DBT-9901): ").strip()
    alias = input("Enter Alphanumeric Alias (e.g., AlphaVaultX): ").strip()
    
    while True:
        try:
            plc_amount = float(input("Enter associated PLC Amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    serial_number = generate_unique_serial(db)
    date_recorded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db[serial_number] = {
        "debt_number": debt_number,
        "alias": alias,
        "plc_amount": plc_amount,
        "date_recorded": date_recorded
    }

    save_db(db)
    print(f"\n[SUCCESS] Generated 6-Digit Serial: {serial_number}\n")

def start_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\n[SERVER RUNNING] Go to: http://localhost:{PORT}")
            print("Press Ctrl+C in this terminal to stop the server.")
            httpd.serve_forever()
    except OSError:
        print(f"\n[ERROR] Port {PORT} is already being used by another app.")
        print("Try closing other terminal windows or restart your code editor.")
    except KeyboardInterrupt:
        print("\nServer shutting down.")

def main():
    init_db()  # Setup empty file immediately
    while True:
        print("=== Debt & PLC System Manager ===")
        print("1. Create New Debt Record")
        print("2. Start Web Server")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            create_debt_record()
        elif choice == '2':
            start_server()
        elif choice == '3':
            break
        else:
            print("Invalid choice.\n")

if __name__ == '__main__':
    main()