import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    course TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT,
    available INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    return_date TEXT,
    returned INTEGER DEFAULT 0
)
""")

conn.commit()


def add_member():
    name = input("Enter member name: ")
    phone = input("Enter phone number: ")
    course = input("Enter course: ")

    cursor.execute(
        "INSERT INTO members (name, phone, course) VALUES (?, ?, ?)",
        (name, phone, course)
    )

    conn.commit()
    print("Member added successfully!")


def view_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    if not members:
        print("No members found.")
        return

    print("\n===== MEMBERS =====")

    for member in members:
        print(
            f"ID: {member[0]} | "
            f"Name: {member[1]} | "
            f"Phone: {member[2]} | "
            f"Course: {member[3]}"
        )


def search_member():
    name = input("Enter member name to search: ")

    cursor.execute(
        "SELECT * FROM members WHERE name LIKE ?",
        ("%" + name + "%",)
    )

    members = cursor.fetchall()

    if not members:
        print("No matching members found.")
        return

    print("\n===== SEARCH RESULTS =====")

    for member in members:
        print(
            f"ID: {member[0]} | "
            f"Name: {member[1]} | "
            f"Phone: {member[2]} | "
            f"Course: {member[3]}"
        )


def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    category = input("Enter category: ")

    cursor.execute(
        "INSERT INTO books (title, author, category) VALUES (?, ?, ?)",
        (title, author, category)
    )

    conn.commit()
    print("Book added successfully!")


def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if not books:
        print("No books found.")
        return

    print("\n===== BOOKS =====")

    for book in books:
        status = "Available" if book[4] == 1 else "Issued"

        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Category: {book[3]} | "
            f"Status: {status}"
        )


def search_book():
    title = input("Enter book title to search: ")

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ("%" + title + "%",)
    )

    books = cursor.fetchall()

    if not books:
        print("No matching books found.")
        return

    print("\n===== SEARCH RESULTS =====")

    for book in books:
        status = "Available" if book[4] == 1 else "Issued"

        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Category: {book[3]} | "
            f"Status: {status}"
        )


def issue_book():
    view_books()

    try:
        book_id = int(input("\nEnter book ID to issue: "))

        cursor.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        )

        book = cursor.fetchone()

        if not book:
            print("Book not found.")
            return

        if book[4] == 0:
            print("Book is already issued.")
            return

        view_members()

        member_id = int(input("\nEnter member ID: "))

        cursor.execute(
            "SELECT * FROM members WHERE id = ?",
            (member_id,)
        )

        member = cursor.fetchone()

        if not member:
            print("Member not found.")
            return

        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)

        cursor.execute("""
            INSERT INTO issued_books
            (book_id, member_id, issue_date, due_date)
            VALUES (?, ?, ?, ?)
        """, (
            book_id,
            member_id,
            issue_date.strftime("%d-%m-%Y"),
            due_date.strftime("%d-%m-%Y")
        ))

        cursor.execute(
            "UPDATE books SET available = 0 WHERE id = ?",
            (book_id,)
        )

        conn.commit()

        print("\nBook issued successfully!")
        print(f"Issue Date: {issue_date.strftime('%d-%m-%Y')}")
        print(f"Due Date: {due_date.strftime('%d-%m-%Y')}")

    except ValueError:
        print("Please enter valid IDs.")


def return_book():
    cursor.execute("""
        SELECT issued_books.id, books.title, members.name,
               issued_books.issue_date, issued_books.due_date
        FROM issued_books
        JOIN books ON issued_books.book_id = books.id
        JOIN members ON issued_books.member_id = members.id
        WHERE issued_books.returned = 0
    """)

    issued = cursor.fetchall()

    if not issued:
        print("No issued books found.")
        return

    print("\n===== ISSUED BOOKS =====")

    for record in issued:
        print(
            f"Issue ID: {record[0]} | "
            f"Book: {record[1]} | "
            f"Member: {record[2]} | "
            f"Issued: {record[3]} | "
            f"Due: {record[4]}"
        )

    try:
        issue_id = int(input("\nEnter issue ID to return: "))

        cursor.execute(
            "SELECT book_id FROM issued_books WHERE id = ? AND returned = 0",
            (issue_id,)
        )

        record = cursor.fetchone()

        if not record:
            print("Issued book record not found.")
            return

        book_id = record[0]
        return_date = datetime.now().strftime("%d-%m-%Y")

        cursor.execute("""
            UPDATE issued_books
            SET return_date = ?, returned = 1
            WHERE id = ?
        """, (return_date, issue_id))

        cursor.execute(
            "UPDATE books SET available = 1 WHERE id = ?",
            (book_id,)
        )

        conn.commit()

        print("Book returned successfully!")
        print(f"Return Date: {return_date}")

    except ValueError:
        print("Please enter a valid issue ID.")


def view_issued_books():
    cursor.execute("""
        SELECT issued_books.id, books.title, members.name,
               issued_books.issue_date, issued_books.due_date
        FROM issued_books
        JOIN books ON issued_books.book_id = books.id
        JOIN members ON issued_books.member_id = members.id
        WHERE issued_books.returned = 0
    """)

    issued = cursor.fetchall()

    if not issued:
        print("No books are currently issued.")
        return

    print("\n===== CURRENTLY ISSUED BOOKS =====")

    for record in issued:
        print(
            f"Issue ID: {record[0]} | "
            f"Book: {record[1]} | "
            f"Member: {record[2]} | "
            f"Issued: {record[3]} | "
            f"Due: {record[4]}"
        )


def view_overdue_books():
    today = datetime.now()

    cursor.execute("""
        SELECT issued_books.id, books.title, members.name,
               issued_books.due_date
        FROM issued_books
        JOIN books ON issued_books.book_id = books.id
        JOIN members ON issued_books.member_id = members.id
        WHERE issued_books.returned = 0
    """)

    issued = cursor.fetchall()

    overdue = []

    for record in issued:
        due_date = datetime.strptime(record[3], "%d-%m-%Y")

        if due_date < today:
            overdue.append(record)

    if not overdue:
        print("No overdue books.")
        return

    print("\n===== OVERDUE BOOKS =====")

    for record in overdue:
        print(
            f"Issue ID: {record[0]} | "
            f"Book: {record[1]} | "
            f"Member: {record[2]} | "
            f"Due Date: {record[3]}"
        )


while True:
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Member")
    print("2. View Members")
    print("3. Search Member")
    print("4. Add Book")
    print("5. View Books")
    print("6. Search Book")
    print("7. Issue Book")
    print("8. Return Book")
    print("9. View Issued Books")
    print("10. View Overdue Books")
    print("11. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_member()

    elif choice == "2":
        view_members()

    elif choice == "3":
        search_member()

    elif choice == "4":
        add_book()

    elif choice == "5":
        view_books()

    elif choice == "6":
        search_book()

    elif choice == "7":
        issue_book()

    elif choice == "8":
        return_book()

    elif choice == "9":
        view_issued_books()

    elif choice == "10":
        view_overdue_books()

    elif choice == "11":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")

conn.close()