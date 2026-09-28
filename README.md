# Library Management System

A Python-based library management application that helps manage library members, books, book issues, returns, and overdue books.

## Features

- Add library members
- View all members
- Search members by name
- Add books
- View all books
- Search books by title
- Track book availability
- Issue books to members
- Automatically calculate due dates
- Return books
- View currently issued books
- Detect overdue books
- Store data using SQLite
- Data remains available after restarting the application

## Technologies Used

- Python
- SQLite
- Git
- GitHub

## Project Structure

```text
library-management
│
├── main.py
├── README.md
├── .gitignore
└── screenshots/

library.db is a local database file and is excluded from Git tracking.

## How to Run
Clone the repository.
Open the project folder in VS Code.
Run:
python main.py

The SQLite database will be created automatically when the application starts.

## Application Menu
1. Add Member
2. View Members
3. Search Member
4. Add Book
5. View Books
6. Search Book
7. Issue Book
8. Return Book
9. View Issued Books
10. View Overdue Books
11. Exit
Data Persistence

Member, book, and issue records are stored in a local SQLite database.

The data remains available even after closing and restarting the application.

## Screenshots
Main Menu

Members and Books

Issued Books

Return and Overdue Books

## Future Improvements
Graphical user interface
Fine calculation for overdue books
Book reservation system
Login and authentication
Export library reports
```
