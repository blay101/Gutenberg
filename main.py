import requests
from urllib import request
import webbrowser
from pathlib import Path

class Database:
    def __init__(self, books, current_page, previous_page, next_page):
        self.books = books
        self.current_page = current_page
        self.previous_page = previous_page
        self.next_page = next_page

    def show_books(self):
        n = 1
        for idx in self.books:
                print(f'{n}: {idx['title']}')
                n += 1

def fetch_url(url):
    response = requests.get(url)
    return response.json()

INITIAL_URL = 'https://gutendex.com/books'

def download_epub(book_data):
    book_url = book_data['formats']['application/epub+zip']
    epub_location = Path(f'./{book_data['title']}')
    if not epub_location.exists():
        request.urlretrieve(book_url, f'{epub_location}.epub')
        return
    else:
        print(f'{epub_location} already exist at selected location\n')
        return

def read_online(book_data):
    text_url = book_data['formats']['text/html']
    #text = request.urlretrieve(text_url, './text')
    webbrowser.open(text_url)


def get_database(response):

    books = response['results']
    next_page = response['next']
    previous_page = response['previous']
    data = Database(books, INITIAL_URL, previous_page, next_page)
    return data

def page_changer(k):
    n = k
    print(f'Showing menu for page {n}')

    if n == 1:
        current_url = 'https://gutendex.com/books'
    else:
        current_url = f'https://gutendex.com/books/?page={n}'

    return current_url

def get_book(database: Database):   
    required_book = []
    while True:
        print("\ntype 'quit' to exit and s to show current books on page")
        title = input('enter title of book: ').lower()
        if title == 'quit': break
        if title == 's': 
            database.show_books()
            continue
        for book in database.books:
            if title in book['title'].lower() or any(title in author.get('name', '').lower() for author in book['authors']):
                required_book.append(book)
        if len(required_book) == 0:
            print(f'\n{title} not found in books catalogue')
            print(f'Try changing to a different page')
            continue
        else:
            print(f'\nPossible suggestions for {title}..\n')
            for index, name in enumerate(required_book):
                print(f'{index + 1}: {name['title']}\n')
            return name

def reading_mode(book_data):
    while True:
        print('1. Read online\n2. Download epub\n3. Back to Main menu')
        choice = int(input('Select your preferred mode '))
        if choice == 1:
            read_online(book_data)
            break
        elif choice == 2:
            download_epub(book_data)
            break
        elif choice == 3:
            return
        else:
            print('\nInvalid selection')
            continue

def intitialize():
    print('\n1. Show books on current page')
    print('2. Search for books')
    print('3. change page')
    print('4. Exit')
    operation = int(input('\nChoose an operation '))

    return operation

def page_information(n):
    inside_active = True
    k = 0
    k += n
    while inside_active:
        option = input('n. next p. previous s. stay d. done ')
        if option == 'n':
            k += 1
            n +=1
            print('switching to next page....')
            print(f'Now on page {n}')
            continue
        elif option == 'p':
            k -= 1
            if k < 1: k = 1
            n -=1
            if n < 1: n = 1
            if k == 1 or n == 1:
                print(f'Now on page {n}\nThis is the initial page')
            print('switching to previous page....')
            print(f'Now on page {n}')
            continue
        elif option == 's':
            k += 0
            n += 0
            print('Staying on current page....')
            print(f'Now on page {n}')
            continue
        elif option == 'd':
            inside_active = False
            break

    return n, k

def main():
    print( '=============================================================')
    print( '             My Gutenberg Database v0.1.0                    ')
    print(  '             Created by Nathaniel Blay                      ')
    print(' =============================================================')

    #url = traverse_page(1)
    response = fetch_url(INITIAL_URL)
    database_information = get_database(response)
    active = True
    n = 1
    while active:
        operation = intitialize()

        if operation == 1:
            database_information.show_books()
            continue
        elif operation == 2:
            book = get_book(database_information)
            reading_mode(book)
            continue
        elif operation == 4:
            active = False
            break
        elif operation == 3:
            n, k = page_information(n)
            url = page_changer(k)
            response = fetch_url(url)
            database_information = get_database(response)
            continue
        else:
            print('Invalid selection. Please try again!')
            continue

    print('\nThanks for stopping by...\nHappy reading :) .')   

if __name__ == '__main__':
    main()

    

# def traverse_page(k):
#     print('Press "n" to move to the next page')
#     print('Press "p" to move to the previous page')
#     print('Press "s" to stay on current Page')
#     print('press "h" to go to home page\n')
#     choice = input("Make your selection ")

#     n = k
#     match choice:
#         case 'n':
#             print('Switching to next page...\n')
#             n += 1
#         case 'p':
#             print('Switching to previous page...\n')
#             n -= 1
#             if n < 1: n = 1
#             print('This is the homepage')
#             print('Staying on page')
#         case 's':
#             n += 0
#         case 'h':
#             n = 1
#         case _:
#             print('invalid response\n')
#             print('Defaulting to current page\n')
#             n += 0

#     if n == 1:
#         current_url = 'https://gutendex.com/books'
#     else:
#         current_url = f'https://gutendex.com/books/?page={n}'

#     return current_url
