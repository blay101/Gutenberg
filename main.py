import requests
from urllib import request
import webbrowser
from pathlib import Path
from operator import itemgetter
import os

class Book:
    def __init__(self, title: str, id: int, authors, summary, subjects, epub_link: str, html_link: str):
        self.title = title
        self.id = id
        self.authors = authors
        self.summary = summary
        self.subjects = subjects
        self.epub_link = epub_link
        self.html_link = html_link

    def get_title(self):
        return self.title

    def get_id(self):
        pass

    def get_authors(self):
        return self.authors[0].get('name')

    def get_summary(self):
        return self.summary[0]

    def get_subjects(self):
        return self.subjects

    def get_epub_link(self):
        return self.epub_link

    def get_html_link(self):
        return self.html_link

        

def fetch_url(url):
    response = requests.get(url)
    return response.json()

INITIAL_URL = 'https://gutendex.com/books'

def download_epub(book: Book) -> None:
    print(f'Downloading {book.get_title()}.....')
    book_url = book.get_epub_link()
    epub_directory = Path(f'./epubs/{book.get_title()}.epub')
    if not epub_directory.exists():
        request.urlretrieve(book_url, f'{epub_directory}')
        print('Download finished')
        return
    else:
        print(f'{book.get_title()}.epub already exist at selected location\n')
        return

def read_online(book: Book) -> None:
    print(f'Opening {book.get_title()} in browser...')
    text_url = book.get_html_link()
    #text = request.urlretrieve(text_url, './text')
    webbrowser.open(text_url)

def get_books(response) -> list[Book]:
    books_data = response['results']
    books = []
    for book in books_data:
        book_title = book['title']
        book_id = book['id']
        book_authors = book['authors']
        book_summary = book['summaries']
        book_subjects = book['subjects']
        book_epub_link = book['formats']['application/epub+zip']
        book_html_link = book['formats']['text/html']
        data = Book(book_title, book_id, book_authors, book_summary, 
                    book_subjects, book_epub_link, book_html_link)
        books.append(data)
    
    return books

def page_changer(k) -> str:
    n = k
    print(f'Showing menu for page {n}')

    if n == 1:
        current_url = 'https://gutendex.com/books'
    else:
        current_url = f'https://gutendex.com/books/?page={n}'

    return current_url

def get_book(books: list[Book]) -> Book | None:   
    required_book = []
    while True:
        print("\nPress 's' to show books on current page")
        print("Press 'q' to go back to main menu")
        title = input('enter title of book: ').lower()
        if title == 'q': break
        if title == 's': 
            for book in books: print(book.get_title())
            continue
        for book in books:
            if title in book.get_title().lower() or any(title in a.get('name', '').lower() for a in book.authors):
                required_book.append(book)
        if len(required_book) == 0:
            print(f'\n{title} not found in books catalogue')
            print(f'Try changing to a different page')
            continue
        else:
            print(f'\nPossible suggestions for {title}..\n')
            for index, book in enumerate(required_book):
                print(f'{index + 1}: {book.get_title()} by {book.get_authors()}')
            try:
                while True:
                    choice = int(input('Make your selection '))
                    
                    try:
                        selected = required_book[choice - 1]
                        print(f'\n{selected.get_title()} selected....')
                        return selected
                    except IndexError:
                        print('\nInvalid selection, please try again')
                        continue

            except ValueError:
                print('\nPlease enter a number')
                return

def reading_mode(book: Book) -> None:
    while True:
        print('1. Read online\n2. Download epub\n3. See book summary')
        print('4. see book subjects')
        print('5. Back to main menu')
        try:
            choice = int(input('Select your preferred mode '))
            if choice == 1:
                read_online(book)
                break
            elif choice == 2:
                download_epub(book)
                break
            elif choice == 3:
                show_summary(book)
                continue
            elif choice == 4:
                show_subjects(book)
                continue
            elif choice == 5:
                return
            else:
                print('\nInvalid selection')
                continue

        except ValueError:
            print('Please enter a number')
            continue
        
def show_summary(book: Book) -> None:
    summary = book.get_summary()
    if summary == '':
        print('No available summary to display')
        return
    print('\nBook sumary\n------------------------------------------')
    print(f'{summary}')

def show_subjects(book: Book) -> None:
    subjects = book.get_subjects()
    if len(subjects) == 0:
        print('No available subjects')
        return
    print('\nBook subjects\n----------------------------------------')
    for subject in subjects:
        print(subject)

def intitialize() -> int | None:
    print('\n1. Show books on current page')
    print('2. Search for books')
    print('3. change page')
    print('4. Exit')
    try:
        operation = int(input('\nChoose an operation '))
    except ValueError:
        print("Invalid selection. Please try again")
        return

    return operation

def page_information(n) -> tuple:
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
            if k != 1 or n !=1 : print('switching to previous page....')
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
    print(  '          Created by Nathaniel Blay(Amadeus)                ')
    print(' =============================================================')

    response = fetch_url(INITIAL_URL)
    books_list = get_books(response)
    
    active = True
    n = 1
    while active:
        operation = intitialize()

        if operation == 1:
            for book in books_list:
                print(book.get_title())
                continue
        elif operation == 2:
            book = get_book(books_list)
            if book:
                reading_mode(book)
                continue
        elif operation == 4:
            active = False
            break
        elif operation == 3:
            n, k = page_information(n)
            url = page_changer(k)
            response = fetch_url(url)
            books_list = get_books(response)
            book = get_book(books_list)
            if book:
                reading_mode(book)
                continue
        else:
            print('Please choose a number from the menu!')
            continue

    print('\nThanks for stopping by...\nHappy reading :) .')   

if __name__ == '__main__':
    main()

