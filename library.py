import json
import os

BOOKS_FILE = "books.json"

def load_books():
    """Loads book data from the JSON file."""
    if not os.path.exists(BOOKS_FILE):
        return []
    try:
        with open(BOOKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{BOOKS_FILE}' was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{BOOKS_FILE}'. File might be corrupted or empty.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading books: {e}")
        return []

def save_books(books):
    """Saves book data to the JSON file."""
    try:
        with open(BOOKS_FILE, 'w') as file:
            json.dump(books, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving books: {e}")

def add_book(books):
    """Adds a new book to the library."""
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    while True:
        try:
            quantity = int(input("Enter quantity: ").strip())
            if quantity < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid quantity. Please enter a non-negative whole number.")

    # Check if book already exists
    for book in books:
        if book['title'].lower() == title.lower() and book['author'].lower() == author.lower():
            book['quantity'] += quantity
            print(f"Book '{title}' by {author} already exists. Quantity updated to {book['quantity']}.")
            save_books(books)
            return

    new_book = {
        "title": title,
        "author": author,
        "quantity": quantity
    }
    books.append(new_book)
    save_books(books)
    print(f"Book '{title}' added successfully.")

def view_all_books(books):
    """Displays all books in the library."""
    if not books:
        print("The library is currently empty.")
        return
    print("\n--- Current Library Catalog ---")
    for i, book in enumerate(books):
        print(f"{i + 1}. Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")
    print("-----------------------------\n")

def find_book(books, search_term, search_by='title'):
    """Helper function to find books by title or author."""
    found_books = []
    for book in books:
        if search_by == 'title' and search_term.lower() in book['title'].lower():
            found_books.append(book)
        elif search_by == 'author' and search_term.lower() in book['author'].lower():
            found_books.append(book)
    return found_books

def lend_book(books):
    """Decreases the quantity of a book after lending."""
    title_or_author = input("Enter title or author of the book to lend: ").strip()
    found_books = find_book(books, title_or_author, search_by='title') + find_book(books, title_or_author, search_by='author')
    
    if not found_books:
        print("Book not found.")
        return

    # Remove duplicates if a book was found by both title and author
    unique_found_books = []
    seen_titles_authors = set()
    for book in found_books:
        identifier = (book['title'].lower(), book['author'].lower())
        if identifier not in seen_titles_authors:
            unique_found_books.append(book)
            seen_titles_authors.add(identifier)

    if len(unique_found_books) > 1:
        print("Multiple books found:")
        for i, book in enumerate(unique_found_books):
            print(f"{i + 1}. Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")
        while True:
            try:
                choice = int(input("Enter the number of the book you want to lend: ").strip()) - 1
                if 0 <= choice < len(unique_found_books):
                    selected_book = unique_found_books[choice]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        selected_book = unique_found_books[0]

    if selected_book['quantity'] > 0:
        selected_book['quantity'] -= 1
        save_books(books)
        print(f"'{selected_book['title']}' by {selected_book['author']} lent successfully. Remaining quantity: {selected_book['quantity']}.")
    else:
        print(f"Error: '{selected_book['title']}' by {selected_book['author']} is currently out of stock.")

def return_book(books):
    """Increases the quantity of a book after return."""
    title_or_author = input("Enter title or author of the book to return: ").strip()
    found_books = find_book(books, title_or_author, search_by='title') + find_book(books, title_or_author, search_by='author')

    if not found_books:
        print("Book not found.")
        return
    
    unique_found_books = []
    seen_titles_authors = set()
    for book in found_books:
        identifier = (book['title'].lower(), book['author'].lower())
        if identifier not in seen_titles_authors:
            unique_found_books.append(book)
            seen_titles_authors.add(identifier)

    if len(unique_found_books) > 1:
        print("Multiple books found:")
        for i, book in enumerate(unique_found_books):
            print(f"{i + 1}. Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")
        while True:
            try:
                choice = int(input("Enter the number of the book you want to return: ").strip()) - 1
                if 0 <= choice < len(unique_found_books):
                    selected_book = unique_found_books[choice]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        selected_book = unique_found_books[0]

    selected_book['quantity'] += 1
    save_books(books)
    print(f"'{selected_book['title']}' by {selected_book['author']} returned successfully. New quantity: {selected_book['quantity']}.")

def delete_book(books):
    """Removes a book record from the library."""
    title_or_author = input("Enter title or author of the book to delete: ").strip()
    found_books = find_book(books, title_or_author, search_by='title') + find_book(books, title_or_author, search_by='author')

    if not found_books:
        print("Book not found.")
        return
    
    unique_found_books = []
    seen_titles_authors = set()
    for book in found_books:
        identifier = (book['title'].lower(), book['author'].lower())
        if identifier not in seen_titles_authors:
            unique_found_books.append(book)
            seen_titles_authors.add(identifier)

    if len(unique_found_books) > 1:
        print("Multiple books found:")
        for i, book in enumerate(unique_found_books):
            print(f"{i + 1}. Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")
        while True:
            try:
                choice = int(input("Enter the number of the book you want to delete: ").strip()) - 1
                if 0 <= choice < len(unique_found_books):
                    book_to_delete = unique_found_books[choice]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        book_to_delete = unique_found_books[0]

    confirm = input(f"Are you sure you want to delete '{book_to_delete['title']}' by {book_to_delete['author']}? (yes/no): ").lower()
    if confirm == 'yes':
        books.remove(book_to_delete)
        save_books(books)
        print(f"Book '{book_to_delete['title']}' deleted successfully.")
    else:
        print("Book deletion cancelled.")

def search_book(books):
    """Searches for a book by title or author."""
    search_term = input("Enter title or author to search for: ").strip()
    found_books = find_book(books, search_term, search_by='title') + find_book(books, search_term, search_by='author')

    unique_found_books = []
    seen_titles_authors = set()
    for book in found_books:
        identifier = (book['title'].lower(), book['author'].lower())
        if identifier not in seen_titles_authors:
            unique_found_books.append(book)
            seen_titles_authors.add(identifier)

    if unique_found_books:
        print("\n--- Search Results ---")
        for book in unique_found_books:
            print(f"Title: {book['title']}, Author: {book['author']}, Quantity: {book['quantity']}")
        print("----------------------\n")
    else:
        print("No books found matching your search term.")

def display_menu():
    """Displays the main menu options."""
    print("\n--- Library Management System ---")
    print("1. Add New Book")
    print("2. View All Books")
    print("3. Lend a Book")
    print("4. Return a Book")
    print("5. Delete a Book")
    print("6. Search for a Book")
    print("7. Exit")
    print("---------------------------------")

def main():
    """Main function to run the Library Management System."""
    books = load_books()

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            add_book(books)
        elif choice == '2':
            view_all_books(books)
        elif choice == '3':
            lend_book(books)
        elif choice == '4':
            return_book(books)
        elif choice == '5':
            delete_book(books)
        elif choice == '6':
            search_book(books)
        elif choice == '7':
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()