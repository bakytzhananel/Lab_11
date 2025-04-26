import psycopg2
import csv


conn = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="your_user",
    password="your_password"
)
cur = conn.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20)
        );
    """)
    conn.commit()


def insert_user_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s);", (name, phone))
    conn.commit()


def insert_from_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            if row:
                cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s);", (row[0], row[1]))
    conn.commit()


def update_user(old_name, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s;", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s;", (new_phone, old_name))
    conn.commit()


def query_phonebook(name_filter=None):
    if name_filter:
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s;", (f"%{name_filter}%",))
    else:
        cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def delete_user(value):
    cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone = %s;", (value, value))
    conn.commit()


if __name__ == "__main__":
    create_table()

    while True:
        print("\nOptions:")
        print("1. Add user (console)")
        print("2. Upload from CSV")
        print("3. Update user")
        print("4. Query users")
        print("5. Delete user")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            insert_user_console()
        elif choice == '2':
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == '3':
            name = input("Enter current user name: ")
            new_name = input("New name (press Enter to skip): ")
            new_phone = input("New phone (press Enter to skip): ")
            update_user(name, new_name if new_name else None, new_phone if new_phone else None)
        elif choice == '4':
            keyword = input("Enter name filter (press Enter to show all): ")
            query_phonebook(keyword if keyword else None)
        elif choice == '5':
            value = input("Enter username or phone to delete: ")
            delete_user(value)
        elif choice == '6':
            break
        else:
            print("Invalid option.")

    cur.close()
    conn.close()
