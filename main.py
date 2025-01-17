""" Program to create and manage a list of books that the user wishes to read, and books that the user has read. """


from bookstore import Book, BookStore, BookError
from sqlite3.dbapi2 import Error, IntegrityError
from menu import Menu
import ui

store = BookStore()
#testing issue2 branch
def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == 'Q':
            break


def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Change Book Read Status', change_read)
    menu.add_option('7', 'Delete Book', delete_book)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_book(): 
    new_book = ui.get_book_info()
    try: # Added a try and except block to prevent the code from crashing if user tries to add a book with an already existing title and author names.
        new_book.save()
        
    except BookError: # if program raises this error, catch it and print this:
        print('\nA book with same tile by the same author already exists.\n')

    

def show_read_books():
    read_books = store.get_books_by_read_value(True)
    ui.show_books(read_books)


def show_unread_books():
    unread_books = store.get_books_by_read_value(False)
    ui.show_books(unread_books)


def show_all_books():
    books = store.get_all_books()
    ui.show_books(books)


def search_book():
    search_term = ui.ask_question('Enter search term, will match partial authors or titles.')
    matches = store.book_search(search_term)
    ui.show_books(matches)


def change_read():

    book_id = ui.get_book_id()
    book = store.get_book_by_id(book_id)
    if book is not None:
        new_read = ui.get_read_value()
        book.read = new_read
        if book.read:
            # If the read status is read, print this:
            print(f'\nYou have read {book.title} by {book.author}\n')
        else: # If the read status is not read, print this:
            print(f'\nYou have not read {book.title} by {book.author}\n')
        book.save()
    else:
        print('\nError: Book Not Found\n')


def delete_book():
    book_id = ui.get_book_id()

    book_deleted = store.get_book_by_id(book_id)
    if book_deleted is None:
        print('Error: Book Not Found')
    else:
        book_deleted.delete()

    

def quit_program():
    ui.message('Thanks and bye!')


if __name__ == '__main__':
    main()
