import sqlite3


# Connect to the SQLite database
def connect_db(db_file="Mbatia_Love.db"):
    conn = sqlite3.connect(db_file)
    return conn


# Query 1: Show all active members
def query_active_members(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Name, PhoneNumber FROM User WHERE MembershipStatus = 'Active';")
    results = cursor.fetchall()
    if results:
        print("Active Members:")
        for row in results:
            print(row)
    else:
        print("No active members found.")


# Query 2: Show all books by a specified author's name or last name
def query_books_by_author_name(conn, author_name):
    cursor = conn.cursor()
    # Use LOWER() to make the search case-insensitive and match any part of the author's name
    cursor.execute("""
        SELECT Book.Title, Book.Length
        FROM Book
        JOIN Author ON Book.AuthorID = Author.AuthorID
        WHERE LOWER(Author.Name) LIKE ?;
    """, (f"%{author_name.lower()}%",))
    results = cursor.fetchall()
    if results:
        print(f"Books by Author matching '{author_name}':")
        for row in results:
            print(row)
    else:
        print(f"No books found for author '{author_name}'.")


# Query 3: Display books rated above a certain rating
def query_books_above_rating(conn, rating):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT B.Title, R.Rating
        FROM Book B
        JOIN Rating R ON B.BookID = R.BookID
        WHERE R.Rating >= ?;
    """, (rating,))
    results = cursor.fetchall()
    if results:
        print(f"Books with Rating {rating} and above:")
        for row in results:
            print(row)
    else:
        print(f"No books found with a rating of {rating} or above.")


# Query 4: Show total number of books checked out
def query_checked_out_books_count(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Book WHERE Availability = 'Checked Out';")
    count = cursor.fetchone()[0]
    print(f"Total books checked out: {count}")


# Query 5: Show rental history for a specified user
def query_rental_history(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Book.Title, RentalService.LoanDate, RentalService.DueDate, RentalService.ReturnedDate
        FROM RentalService
        JOIN Book ON RentalService.BookID = Book.BookID
        WHERE RentalService.MemberID = ?;
    """, (user_id,))
    results = cursor.fetchall()
    if results:
        print(f"Rental history for User {user_id}:")
        for row in results:
            print(row)
    else:
        print(f"No rental history found for user '{user_id}'.")


# Query 6: Show all books with their authors
def query_all_books_with_authors(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Book.Title, Author.Name
        FROM Book
        JOIN Author ON Book.AuthorID = Author.AuthorID;
    """)
    results = cursor.fetchall()
    if results:
        print("Books and their Authors:")
        for row in results:
            print(f"Book: {row[0]}, Author: {row[1]}")
    else:
        print("No books found.")


# Main function to execute queries
def main():
    conn = connect_db()

    while True:
        print("\nChoose a query to execute:")
        print("1. Show all active members")
        print("2. Show all books by a specified author")
        print("3. Display books rated above a certain rating")
        print("4. Show total number of books checked out")
        print("5. Show rental history for a specified user")
        print("6. Show all books with their authors")
        print("7. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            query_active_members(conn)
        elif choice == '2':
            author_name = input("Enter Author's Name or Last Name: ")
            query_books_by_author_name(conn, author_name)
        elif choice == '3':
            try:
                rating = int(input("Enter minimum rating (1-5): "))
                if 1 <= rating <= 5:
                    query_books_above_rating(conn, rating)
                else:
                    print("Please enter a valid rating between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter an integer between 1 and 5.")
        elif choice == '4':
            query_checked_out_books_count(conn)
        elif choice == '5':
            user_id = input("Enter UserID: ")
            query_rental_history(conn, user_id)
        elif choice == '6':
            query_all_books_with_authors(conn)
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    conn.close()


if __name__ == "__main__":
    main()
