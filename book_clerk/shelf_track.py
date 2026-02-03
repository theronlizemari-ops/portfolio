'''
This programme is called the Book Clerk. It allows a bookstore manager to
do the following:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    5. View details of all books

This task showcases basic SQLite commands, including:
    CREATE TABLE
    INSERT INTO
    UPDATE
    SELECT FROM
    INNER JOIN
    DROP TABLE
'''

import sqlite3


# ====== Functions ======
def create_book_table():
    '''Code to create a table at the start of the program.'''

    # To run my code miltiple times
    cursor.execute('''DROP TABLE IF EXISTS book''')

    # Create table "book"
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY CHECK (id BETWEEN 1000 AND 9999),
            title TEXT,
            authorID INTEGER,
            qty INTEGER DEFAULT 0
        )
        '''
        )
    db.commit()

    # Populate table
    book_data = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice in Wonderland", 5620, 12)
    ]

    cursor.executemany(
        '''
        INSERT INTO book(id, title, authorID, qty)
        VALUES(?, ?, ?, ?)
        ''',
        book_data
    )

    db.commit()


def create_author_table():
    '''Code to create a table at the start of the program.'''
    # To run my code miltiple times
    cursor.execute('''DROP TABLE IF EXISTS author''')

    # Create table "author"
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY CHECK (id BETWEEN 1000 AND 9999),
            name TEXT,
            country TEXT)
        ''')
    db.commit()

    # Populate table
    author_data = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")
    ]

    cursor.executemany(
        '''
        INSERT INTO author(id, name, country)
        VALUES(?, ?, ?)
        ''',
        author_data
    )

    db.commit()


def enter_book():
    '''This function allows the user to enter a new book in the database.
    Users can also enter a new author if the author isn't in the
    database.'''

    while True:
        try:
            # Book info
            book_id = int(input("Enter book ID: "))
            book_title = input("Enter book title: ")
            author_id = int(input("Enter author ID: "))
            book_qty = int(input("Enter quantity: "))
            # Check if author exists
            cursor.execute(
                '''SELECT id, name, country FROM author
                WHERE id = ?''', (author_id,))
            author = cursor.fetchone()

            if author is None:
                # Author not found, ask user if they want to add a new author
                add_author = input(
                    f"Author with ID {author_id} does not exist. "
                    "Do you want to add this author? (yes/no) "
                ).strip().lower()

                while True:
                    if add_author == "yes":
                        author_name = input("Enter author's name: ")
                        author_country = input("Enter author's country: ")

                        cursor.execute(
                            '''INSERT INTO author(id, name, country)
                            VALUES(?, ?, ?)''',
                            (author_id, author_name, author_country)
                        )
                        print(f"\nAuthor {author_name} added.")

                        db.commit()
                        break

                    elif author == "no":
                        print("Please enter the correct author ID.")
                        continue  # Go back to start of the loop

                    else:
                        print("Invalid input. Please try again.")

            # Insert the book
            cursor.execute(
                '''INSERT INTO book(id, title, authorID, qty)
                VALUES(?, ?, ?, ?)''',
                (book_id, book_title, author_id, book_qty)
            )
            db.commit()
            print(f"\nBook '{book_title}' with ID {book_id} added.")
            break

        except (ValueError, sqlite3.IntegrityError) as e:
            print(f"Error: {e}. Please start again.")


def update_book():
    '''This function is to update books in the database. Users can update
    the quantity of books, the title, the author's ID  as well as the
    author's name and country.'''

    while True:
        try:
            update_select = int(input(
                '''\nPlease select what you want to update:
1 - Update quantity
2 - Update title
3 - Update author's ID
4 - Review author's name and country
0 - Exit
Choice: '''))

        except ValueError:
            print("Could not make that selection. Please try again.")
            continue

        if update_select == 0:
            print("\nExiting update menu.")
            break

        if update_select == 1:  # Update quantity
            while True:
                try:
                    print("\nUPDATE QUANTITY OF BOOKS")
                    add_id = int(input("Enter the book's ID: "))
                    add_qty = int(input("How many books are you adding? "))

                    cursor.execute(
                        '''UPDATE book SET qty = qty + ? WHERE id = ?''',
                        (add_qty, add_id)
                    )
                    db.commit()

                    if cursor.rowcount == 0:
                        print(f"No book found with ID {add_id}. "
                              "Please try again.")
                        continue

                    print(f"Quantity updated for book ID {add_id}.")
                    break

                except ValueError:
                    print("Please enter a valid number.")

        elif update_select == 2:  # Update title
            while True:
                try:
                    print("\nUPDATE TITLE OF BOOK")
                    change_id = int(input("Enter the book's ID: "))
                    change_title = input("Enter new title: ")

                    cursor.execute(
                        '''UPDATE book SET title = ? WHERE id = ?''',
                        (change_title, change_id)
                    )
                    db.commit()

                    if cursor.rowcount == 0:
                        print(f"No book found with ID {change_id}. "
                              "Please try again.")
                        continue

                    print(f"Title updated for book ID {change_id}.")
                    break

                except ValueError:
                    print("Invalid input. Please try again.")

        elif update_select == 3:  # Update author ID
            while True:
                try:
                    print("UPDATE AUTHOR'S ID")
                    update_id = int(input("Enter the book's ID: "))
                    update_author = int(input("Enter author's ID: "))

                    cursor.execute(
                        '''UPDATE book SET authorID = ? WHERE id = ?''',
                        (update_author, update_id))
                    db.commit()

                    if cursor.rowcount == 0:
                        print(f"No book found with ID {update_id}. "
                              "Please try again.")
                        continue

                    print(f"Author ID updated for book ID {update_id}.")
                    break

                except ValueError:
                    print("Invalid input. Please enter numbers only.")

        elif update_select == 4:
            while True:
                try:
                    print("REVIEW AUTHOR'S NAME AND COUNTRY")
                    view_nc = int(input("Enter book's ID: "))

                    cursor.execute(
                        '''SELECT book.id, author.name,
                        author.country, author.id
                        FROM book
                        INNER JOIN author
                        ON book.authorID = author.id
                        WHERE book.id = ?''', (view_nc,))

                    to_view = cursor.fetchone()

                    if to_view is None:
                        print(f"No book found with ID {view_nc}. "
                              "Please try again.\n")
                        continue

                    book_id, author_name, author_country, author_id = to_view

                    print(f"\nBook ID:          {book_id}"
                          f"\nAuthor's name:    {author_name}"
                          f"\nAuthor's country: {author_country}")

                    while True:
                        update_nc = input("\nDo you want to update this info? "
                                          "(yes/no) ").lower()

                        if update_nc == "yes":
                            while True:
                                up_nc = input("Enter n for name or "
                                              "c for country: ").lower()

                                if up_nc == "n":
                                    print("\nUPDATE AUTHOR'S NAME")
                                    new_name = input("Enter name: ")
                                    cursor.execute(
                                        '''UPDATE author
                                        SET name = ?
                                        WHERE id = ?''',
                                        (new_name, author_id)
                                    )
                                    db.commit()
                                    print("Author's name updated.")
                                    break

                                elif up_nc == "c":
                                    print("\nUPDATE AUTHOR'S COUNTRY")
                                    new_country = input("Enter new country: ")

                                    cursor.execute(
                                        '''UPDATE author
                                        SET country = ?
                                        WHERE id = ?''',
                                        (new_country, author_id)
                                    )
                                    db.commit()
                                    print("Author's country updated.")
                                    break

                                else:
                                    print("Invalid selection. "
                                          "Please enter n or c.")
                            break

                        elif update_nc == "no":
                            print("No updates made.")
                            break

                        else:
                            print("Invalid input. Please try again.")
                    break

                except ValueError:
                    print("Invalid input. Please enter numbers only.")
        else:
            print("Invalid selection. Please try again.")


def delete_book():
    '''This function is to delete a book using their ID. The code checks
    to make sure that the users wants to delete the book, as well as
    validate data and error handeling.'''

    while True:
        try:
            del_book = int(input("Enter book's ID: "))
            cursor.execute('''
                           SELECT title FROM book WHERE id = ?''',
                           (del_book,))
            show_title = cursor.fetchone()
            if show_title:
                print(f'The book with {del_book} is titled: {show_title[0]}\n')
                confirm = input("Is this the book you want to delete? "
                                "(yes/no) ").lower()
                if confirm == "yes":
                    cursor.execute('''
                                   DELETE FROM book WHERE id = ?''',
                                   (del_book,))
                    db.commit()
                    print(f'\nBook with ID {del_book} deleted.\n')
                    break
                elif confirm == "no":
                    continue
                else:
                    print("Invalid input. Please try again.")
            else:
                print(f'No book found with ID {del_book}.\n')

        except ValueError:
            print("Invalid input. Please try again.")


def search_books():
    '''This function is to search for a book using the book's ID.'''

    while True:
        try:
            search_book = int(input("Enter book's ID: "))

            cursor.execute('''
                SELECT id, title, authorID, qty
                FROM book
                WHERE id = ?
            ''', (search_book,))

            dis_book = cursor.fetchall()

            for row in dis_book:
                print(f"ID: {row[0]}, Title: {row[1]}, "
                      f"AuthorID: {row[2]}, Qty: {row[3]}")
                return

            if not dis_book:
                print(f"No book found with ID {search_book}. "
                      "Please try again.")
                continue

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def view_all():
    '''This function is to view all the books in the database.'''

    # INNER JOIN to fetch book title, author's name, and country
    cursor.execute("""
        SELECT book.title, author.name, author.country
        FROM book
        INNER JOIN author
        ON book.authorID = author.id
    """)

    results = cursor.fetchall()

    # Display the results:
    if results:
        titles, names, countries = zip(*results)

        print("\n--- BOOK DETAILS ---\n")
        for title, name, country in zip(titles, names, countries):
            print(f"Title:   {title}"
                  f"\nAuthor:  {name}"
                  f"\nCountry: {country}\n")
    else:
        print("No books found.")


# ======= Main ===========
# Create database
db = sqlite3.connect("ebookstore.db")
cursor = db.cursor()

# Create tables
create_book_table()
create_author_table()

# User menu
while True:
    try:
        menu_select = int(input('''
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit

Choice: '''))
        if menu_select == 1:
            enter_book()

        elif menu_select == 2:
            update_book()

        elif menu_select == 3:
            delete_book()

        elif menu_select == 4:
            search_books()

        elif menu_select == 5:
            view_all()

        elif menu_select == 0:
            db.close()
            break

        else:
            print("Invalid input. Please try again.")

    except ValueError:
        print("Invalid input. Please enter a number.")
