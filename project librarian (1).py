import datetime
import os
import sys
import random
import csv
import json
import tempfile
import shutil


RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
ORANGE = '\033[38;5;208m'
VIOLET = '\033[38;5;135m'
BOLD = '\033[1m'
RESET = '\033[0m'

def rprint(msg, end='\n'):
    print(f"{RED}{msg}{RESET}", end=end)

def gprint(msg, end='\n'):
    print(f"{GREEN}{msg}{RESET}", end=end)

def bprint(msg, end='\n'):
    print(f"{BOLD}{msg}{RESET}", end=end)

def blprint(msg, end='\n'):
    print(f"{BOLD}{BLUE}{msg}{RESET}", end=end)

def oprint(msg, end='\n'):
    print(f"{ORANGE}{msg}{RESET}", end=end)

def vprint(msg, end='\n'):
    print(f"{VIOLET}{msg}{RESET}", end=end)

BOOKS_PATH = 'books123.updated.csv'
PATRONS_PATH = 'patron1.csv'
LIBRARIANS_PATH = 'librarian1.csv'
ASSISTANTS_PATH = 'assistant1.csv'
TRANSACTIONS_PATH = 'transactions.csv'

if not os.path.exists(PATRONS_PATH) or os.path.getsize(PATRONS_PATH) == 0:
    with open(PATRONS_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'age', 'library_number', 'fines',
            'days_overdue', 'max_books_allowed', 'max_days_allowed',
            'contact_number', 'book_preferences', 'borrowed_books', 'object'
        ])
if not os.path.exists(ASSISTANTS_PATH) or os.path.getsize(ASSISTANTS_PATH) == 0:
    with open(ASSISTANTS_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'username', 'password', 'library_number', 'object'])
if not os.path.exists(LIBRARIANS_PATH) or os.path.getsize(LIBRARIANS_PATH) == 0:
    with open(LIBRARIANS_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'username', 'password', 'library_number', 'object'])


if not os.path.exists(BOOKS_PATH):
    rprint("INSTALL books123.updated.csv FIRST IN UVLE AND OPEN IT IN SAME FOLDER")
    sys.exit(1)

_fines_collected = 0.0
_current_user = None
_current_client = None

def init_transactions(path=TRANSACTIONS_PATH):
    import csv, os
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp','type','actor_username','patron_library_number','bookID','amount','note'])

def log_transaction(t_type, actor_username=None, patron_library_number=None, bookID=None, amount=0.0, note=None, path=TRANSACTIONS_PATH):
    import csv, os
    init_transactions(path)
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([ts, t_type, actor_username or '', patron_library_number or '', bookID or '', f"{amount}", note or ''])

def view_transactions(limit=50, path=TRANSACTIONS_PATH):
    import csv, os
    init_transactions(path)
    rows = []
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows[-limit:][::-1]

init_transactions()


def corrector(path=PATRONS_PATH):
    setted = ['name', 'age', 'library_number', 'fines',
                'days_overdue', 'max_books_allowed', 'max_days_allowed',
                'contact_number', 'book_preferences', 'borrowed_books', 'object']
    
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(setted)
        return

    
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        with open(path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(setted)
        return

    current_header = [h.strip() for h in rows[0]]
    if current_header == setted:
        return

   
    new_rows = [setted]
    for r in rows[1:]:
        mapping = {}
        for i, h in enumerate(current_header):
            mapping[h] = r[i] if i < len(r) else ''
        new_row = [mapping.get(col, '') for col in setted]
        new_rows.append(new_row)

    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

def clear_screen():
   
    if os.name == 'nt':
        os.system('cls')

    else:
     os.system('clear')


current_user = None
current_client = None

def set_current_user(user):
    global _current_user, current_user
    _current_user = user
    current_user = user

def get_current_user():
    return current_user if current_user is not None else _current_user

def set_current_client(client):
    global _current_client, current_client
    _current_client = client
    current_client = client

def get_current_client():
    return current_client if current_client is not None else _current_client
class Book:
    def __init__(self, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count, text_reviews_count, publication_date, publisher):
        self._title = title
        self._authors = authors
        self._average_rating = average_rating
        self._isbn = isbn
        self._isbn13 = isbn13
        self._language_code = language_code
        self._num_pages = num_pages
        self._ratings_count = ratings_count
        self._text_reviews_count = text_reviews_count
        self._publication_date = publication_date
        self._publisher = publisher

    @property
    def title(self):
        return self._title
    
    @property
    def authors(self):
        return self._authors
    
    @property
    def isbn(self):
        return self._isbn
    
    @property
    def isbn13(self):
        return self._isbn13
    
    def get(self, key, default=''):
        attr_map = {
            'title': self._title,
            'authors': self._authors,
            'average_rating': self._average_rating,
            'isbn': self._isbn,
            'isbn13': self._isbn13,
            'language_code': self._language_code,
            'num_pages': self._num_pages,
            'ratings_count': self._ratings_count,
            'text_reviews_count': self._text_reviews_count,
            'publication_date': self._publication_date,
            'publisher': self._publisher
        }
        return attr_map.get(key, default)

_books = []

with open(BOOKS_PATH, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        
        clean_row = {k.strip(): (v.strip() if v and isinstance(v, str) else v) for k, v in row.items() if k}
        
        if not clean_row.get('title') or not clean_row.get('isbn'):
            continue
        
        try:
            book = Book(
                title = clean_row.get('title', ''),
                authors = clean_row.get('authors', ''),
                average_rating = float(clean_row.get('average_rating', 0)) if clean_row.get('average_rating') else 0.0,
                isbn = clean_row.get('isbn', ''),
                isbn13 = clean_row.get('isbn13', ''),
                language_code = clean_row.get('language_code', ''),
                num_pages = int(clean_row.get('num_pages', 0)) if clean_row.get('num_pages') else 0,
                ratings_count = int(clean_row.get('ratings_count', 0)) if clean_row.get('ratings_count') else 0,
                text_reviews_count = int(clean_row.get('text_reviews_count', 0)) if clean_row.get('text_reviews_count') else 0,
                publication_date = clean_row.get('publication_date', ''),
                publisher = clean_row.get('publisher', '')
            )
            _books.append(book)
        except (ValueError, KeyError):
            continue

_used_library_numbers = set()
def _generate_library_number():
    while True:
        num = random.randint(10000, 99999)
        if num not in _used_library_numbers:
            _used_library_numbers.add(num)
            return num


generate_library_number = _generate_library_number
used_library_numbers = _used_library_numbers

for _p in (PATRONS_PATH, LIBRARIANS_PATH, ASSISTANTS_PATH):
    try:
        if os.path.exists(_p) and os.path.getsize(_p) > 0:
            with open(_p, mode='r', encoding='utf-8', newline='') as _f:
                _r = csv.DictReader(_f)
                for _row in _r:
                    _v = _row.get('library_number')
                    if _v:
                        try:
                            _used_library_numbers.add(int(str(_v).strip()))
                        except Exception:
                            pass
    except Exception:
        pass

class Person:
    def __init__(self, name, age):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name
    
    @property
    def age(self):
        return self._age

class Staff(Person):

    def __init__(self, name, age, username, password):
        super().__init__(name, age)
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Username must be a non-empty string")
        if not isinstance(password, str) or len(password) < 1:
            raise ValueError(f"{RED}Password must be at least 1 character{RESET}")
        self._username = username
        self._password = password
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    
    def set_password(self, new_password):
        if not isinstance(new_password, str) or len(new_password) < 1:
            raise ValueError(f"{RED}Password must be at least 1 character{RESET}")
        self._password = new_password
    def search_book(self):
             
            import os, csv
            clear_screen()
            print("Search Books")
        
            books_path = 'books123.updated.csv'
            if not os.path.exists(books_path):
                print("Books file not found.")
                input(f"{GREEN}\nPress Enter to return to menu...{RESET}")
                return
        
            bprint("Search by:")
            print("1. Book number")
            print("2. Title")
            print("3. ISBN")
            choice = input(f"{GREEN}Choose an option (1-3) or B to cancel:{RESET} ").strip().lower()
            if not choice or choice == 'b':
                return
        
            def share_detail_book(b):
                lines = []
                lines.append(f"Book ID: {b.get('bookID','')}")
                lines.append(f"Title: {b.get('title','')}")
                lines.append(f"Authors: {b.get('authors','')}")
                lines.append(f"Average Rating: {b.get('average_rating','')}")
                lines.append(f"ISBN: {b.get('isbn','')}  ISBN13: {b.get('isbn13','')}")
                lines.append(f"Pages: {b.get('num_pages','')}  Language: {b.get('language_code','')}")
                lines.append(f"Ratings: {b.get('ratings_count','')}  Reviews: {b.get('text_reviews_count','')}")
                lines.append(f"Publication Date: {b.get('publication_date','')}  Publisher: {b.get('publisher','')}")
                lines.append(f"Status: {b.get('Status', b.get('status',''))}  Checkouts: {b.get('Checkouts','')} ")
                return '\n'.join(lines)
        
            def show_the_book(b, width_title=48, width_auth=20):
                bid = str(b.get('bookID','')).ljust(6)
                title = (b.get('title','') or '')[:width_title].ljust(width_title)
                authors = (b.get('authors','') or '')[:width_auth].ljust(width_auth)
                isbn = (b.get('isbn','') or '').ljust(13)
                status = (b.get('Status') or b.get('status') or '').ljust(12)
                return f"{bid}  {title}  {authors}  {isbn}  {status}"
        
            with open(books_path, mode='r', encoding='utf-8', newline='') as bf:
                reader = csv.DictReader(bf)
                rows = list(reader)
        
            if choice == '1':
                bid = input(f"{GREEN}Enter Book ID (exact) or B to cancel:{RESET} ").strip()
                if not bid or bid.lower() == 'b':
                    return
                match = next((r for r in rows if (r.get('bookID') or '').strip() == bid), None)
                if not match:
                    rprint(f"No book found with Book ID '{bid}'.")
                    input(f"{GREEN}\nPress Enter to return to menu...{RESET}")
                    return
                clear_screen()
                bprint(share_detail_book(match))
                input(f"{GREEN}\n\nPress Enter to return to menu...{RESET}")
                return
        
            mapperr = {'2': 'title', '3': 'isbn'}
            field = mapperr.get(choice)
            if not field:
                rprint("Invalid choice.")
                return
        
            term = input(f"{GREEN}Enter search term for {field} (case-insensitive) or B to cancel:{RESET} ").strip()
            if not term or term.lower() == 'b':
                return
        
            term_lower = term.lower()
            def matches_term(r):
                return term_lower in (r.get(field) or '').lower()
        
            matched = [r for r in rows if matches_term(r)]
            if not matched:
                rprint("No matches found.")
                input(f"{GREEN}\nPress Enter to return to menu...{RESET}")
                return
        
            page = 0
            page_size = 10
            total = len(matched)
            while True:
                clear_screen()
                start = page * page_size
                end = min(start + page_size, total)
                page_items = matched[start:end]
        
                print(f"Showing results {start+1}-{end} of {total} for '{term}' (field: {field})")
                bprint("BookID  Title                                             Authors              ISBN          Status       Checkouts")
                print("------  " + "-"*48 + "  " + "-"*20 + "  " + "-"*13 + "  " + "-"*12 + "  " + "-"*9)
                for r in page_items:
                    print(show_the_book(r) + "  " + str(r.get('Checkouts', '')))

                print(f"{GREEN}\nOptions: enter a Book ID to view details, 'N' next, 'P' previous, 'B' back to menu{RESET}")
                searcherr = input("Choice: ").strip()

                if not searcherr:
                    continue
                loweringg = searcherr.lower()
                if loweringg == 'b':
                    return
                if loweringg == 'n':
                    if end >= total:
                        rprint("No more pages.")
                        continue
                    page += 1
                    continue
                if loweringg == 'p':
                    if page == 0:
                        print("Already at first page.")
                        continue
                    page -= 1
                    continue

                chosen = next((m for m in matched if (m.get('bookID') or '').strip() == searcherr), None)
                if chosen:
                    clear_screen()
                    bprint(share_detail_book(chosen))
                    input(f"{GREEN}\n\nPress Enter to return to results...{RESET}")
                    try:
                        index_selectt = matched.index(chosen)
                        page = index_selectt // page_size
                    except Exception:
                        pass
                    continue

                rprint("Invalid input or Book ID not in results.")
                continue

    def change_password(self):
        clear_screen()
        print("Change Password")
        current_password = input(f"{GREEN}Enter current password:{RESET} ")
        if current_password != self.password:
            rprint("Incorrect current password.")
            return
        new_password = input(f"{GREEN}Enter new password:{RESET} ")
        confirm_password = input(f"{GREEN}Confirm new password:{RESET} ")
        if new_password != confirm_password:
            rprint("New passwords do not match.")
            return

        path = 'librarian1.csv' if isinstance(self, Librarian) else 'assistant1.csv'
        with open(path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            records = list(reader)

        with open(path, mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                if record['username'] == self.username:
                    record['password'] = new_password
                writer.writerow(record)

        self.set_password(new_password)
        blprint("Password changed successfully.")

    def add_book(self):
        books = read(BOOKS_PATH)
        print("Add New Book")

        while True:
            title = input(f"{GREEN}Enter book title (or B to cancel):{RESET} ").strip()
            if not title or title.lower() == 'b':
                blprint("Aborted.")
                return

            authors = input(f"{GREEN}Enter author:{RESET} ").strip()

            while True:
                isbn = input(f"{GREEN}Enter ISBN: {RESET}").strip()
                isbn13 = input(f"{GREEN}Enter ISBN13: {RESET}").strip()

                if not isbn and not isbn13:
                    rprint("At least one of ISBN or ISBN13 must be provided.")
                    continue

                parehas = False
                for b in books:
                    if isbn and b['isbn'] == isbn:
                        rprint("A book with this ISBN already exists.")
                        parehas = True
                        break
                    if isbn13 and b['isbn13'] == isbn13:
                        rprint("A book with this ISBN13 already exists.")
                        parehas = True
                        break
                if parehas:
                    continue
                break

            language_code = input(f"{GREEN}Enter language code ('en' is default):{RESET} ").strip()
            if not language_code:
                language_code = 'en'
            
            publisher = input(f"{GREEN}Enter publisher:{RESET} ").strip()
            publication_date = input(f"{GREEN}Enter publication date (MM/DD/YYYY):{RESET} ").strip()

            try:
                num_pages = int(input(f"{GREEN}Enter number of pages:{RESET} ").strip())
            except ValueError:
                num_pages = 0

            try:
                average_rating = float(input(f"{GREEN}Enter average rating (0.0 - 5.0): {RESET}").strip())
            except ValueError:
                average_rating = 0.0

            try:    
                ratings_count = int(input(f"{GREEN}Enter ratings count: {RESET}").strip())
            except ValueError:
                ratings_count = 0

            try:
                text_reviews_count = int(input(f"{GREEN}Enter text reviews count: {RESET}").strip())  
            except ValueError:
                text_reviews_count = 0

            
            rows = read(BOOKS_PATH)
            max_id = 0

            for row in rows:
                try:
                    if 'bookID' in row and row['bookID'].strip().isdigit():
                        book_id = int(row['bookID'].strip())
                        if book_id > max_id:
                            max_id = book_id
                except (ValueError, KeyError):
                    continue
            
            new_book_id = max_id + 1
            blprint(f"Assigned Book ID: {new_book_id}")

            fieldnames = [
        'bookID', 'title', 'authors', 'average_rating', 'isbn', 'isbn13',
        'language_code', 'num_pages', 'ratings_count', 'text_reviews_count',
        'publication_date', 'publisher', 'Status', 'Checkouts'
    ]
            new_book = {
            'bookID': new_book_id,
            'title': title,
            'authors': authors,
            'average_rating': average_rating,
            'isbn': isbn,
            'isbn13': isbn13,
            'language_code': language_code,
            'num_pages': num_pages,
            'ratings_count': ratings_count,
            'text_reviews_count': text_reviews_count,
            'publication_date': publication_date,
            'publisher': publisher,
            'Status': 'Available',
            'Checkouts': 0
    }
            try:
                with open(BOOKS_PATH, mode='a', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    if os.path.getsize(BOOKS_PATH) == 0:
                        writer.writeheader()
                    writer.writerow(new_book)
                blprint(f"Book added successfully with Book ID: {new_book_id}")
            except Exception as e:
                print("Error adding book:", str(e))
                return
            
            try:
                new_book_obj = Book(
                title, authors, average_rating, isbn, isbn13, 
                language_code, num_pages, ratings_count, 
                text_reviews_count, publication_date, publisher
            )
                books.append(new_book_obj)
            except Exception as e:
                print("Error creating book object:", str(e))

            break
        

        
    def remove_book(self):
        import csv, os, tempfile, shutil

        print("Remove a Book")

        book_id_to_remove = input(f"{GREEN}Enter Book ID to remove (or B to cancel): {RESET}").strip()
        if not book_id_to_remove or book_id_to_remove.lower() == 'b':
            blprint("Aborted.")
            return

        if not book_id_to_remove.isdigit():
            rprint("Invalid Book ID.")
            return

        found_title = None
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8')
        removed = False

        try:
            with open(BOOKS_PATH, mode='r', encoding='utf-8', newline='') as f, temp_file:
                reader = csv.DictReader(f)
                writer = csv.DictWriter(temp_file, fieldnames=reader.fieldnames)
                writer.writeheader()

                for row in reader:
                    if (row.get('bookID') or '').strip() == book_id_to_remove:
                        found_title = row.get('title', '')
                        removed = True
                        continue
                    writer.writerow(row)

            if not removed:
                os.remove(temp_file.name)
                rprint(f"No book found with Book ID {book_id_to_remove}.")
                return

            confirm = input(f"{GREEN}Are you sure you want to remove '{found_title}' (Book ID: {book_id_to_remove})? (y/N):{RESET} "
            ).strip().lower()

            if confirm != 'y':
                os.remove(temp_file.name)
                blprint("Removal cancelled.")
                return

            shutil.move(temp_file.name, BOOKS_PATH)
            blprint(f"✓ Book ID {book_id_to_remove} removed successfully.")

        except Exception as e:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
            rprint("Error removing book:", e)
            return

        _books.clear()
        with open(BOOKS_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    _books.append(Book(
                        r.get('title',''),
                        r.get('authors',''),
                        float(r.get('average_rating') or 0),
                        r.get('isbn',''),
                        r.get('isbn13',''),
                        r.get('language_code',''),
                        int(r.get('num_pages') or 0),
                        int(r.get('ratings_count') or 0),
                        int(r.get('text_reviews_count') or 0),
                        r.get('publication_date',''),
                        r.get('publisher','')
                    ))
                except Exception:
                    pass




    def delete_own_account(self):
        clear_screen()
        username = self.username
        confirm = input(f"{GREEN}Are you sure you want to delete your account '{username}'? This action cannot be undone. (y/N):{RESET} ").strip().lower()
        if confirm != 'y':
            blprint("Account deletion aborted.")
            return

        path = 'librarian1.csv' if isinstance(self, Librarian) else 'assistant1.csv'
        with open(path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            records = list(reader)

        with open(path, mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            removed = False
            for record in records:
                if record['username'] != username:
                    writer.writerow(record)
                else:
                    removed = True

            if removed:
                blprint(f'Account with username {username} deleted successfully.')
            else:
                rprint(f'Account with username {username} not found.')

    def calculate_overdue_fines(self):
        import csv, json, datetime, tempfile, shutil, os

        clear_screen()
        print("Calculate Overdue Fines")

        patron_path = 'patron1.csv'
        fine_per_day = 5
        today = datetime.date.today()

        with open(patron_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            patrons = list(reader)
            fieldnames = reader.fieldnames

        for p in patrons:
            try:
                borrowed = json.loads(p.get('borrowed_books') or '{}')
            except Exception:
                borrowed = {}

            total_days_overdue = 0
            total_fine = 0

            for info in borrowed.values():
                try:
                    due = datetime.date.fromisoformat(info.get('due_date', ''))
                except Exception:
                    continue

                if today > due:
                    days = (today - due).days
                    total_days_overdue += days
                    total_fine += days * fine_per_day

            p['days_overdue'] = str(total_days_overdue)
            p['fines'] = str(float(p.get('fines') or 0) + total_fine)

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(patrons)
        shutil.move(tmp, patron_path)

        print("✓ Overdue fines calculated.")
        print()
        bprint("Fines summary:")
        total_outstanding = 0.0
        for p in patrons:
            try:
                fines_amt = float(p.get('fines') or 0.0)
            except Exception:
                fines_amt = 0.0
            name = p.get('name') or 'Unknown'
            libno = p.get('library_number') or ''
            print(f" - {name} ({libno}): ₱{fines_amt:.2f}")
            total_outstanding += fines_amt

        bprint(f"\nTotal outstanding fines: ₱{total_outstanding:.2f}")

            
    def lend_book(self):
        import csv, json, datetime, tempfile, shutil, os

        clear_screen()
        print("Lend a Book")

        lib_no = input(f"{GREEN}Enter patron library number (or B to cancel):{RESET} ").strip()
        if not lib_no or lib_no.lower() == 'b':
            return

        patron_path = 'patron1.csv'
        with open(patron_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            patrons = list(reader)
            fieldnames = reader.fieldnames

        patron = next((p for p in patrons if p.get('library_number') == lib_no), None)
        if not patron:
            rprint("Patron not found.")
            return

        try:
            borrowed = json.loads(patron.get('borrowed_books') or '{}')
        except Exception:
            borrowed = {}

        if len(borrowed) >= int(patron.get('max_books_allowed') or 0):
            print("Borrowing limit reached.")
            return

        book_id = input(f"{GREEN}Enter Book ID to lend:{RESET}").strip()
        if not book_id:
            return

        with open(BOOKS_PATH, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            books = list(reader)
            book_fields = reader.fieldnames

        book = next((b for b in books if (b.get('bookID') or '').strip() == book_id), None)
        if not book:
            rprint("Book not found.")
            return

        status_lower = (book.get('Status') or '').strip().lower()
        if status_lower == 'checked out':
            rprint("Book already checked out.")
            return
        if status_lower == 'reserved':
            rprint("Book is reserved and cannot be lent.")
            return
        if status_lower == 'lost':
            rprint("Book is marked lost and cannot be lent.")
            return

        today = datetime.date.today()
        max_days = int(patron.get('max_days_allowed') or 0)
        due_date = (today + datetime.timedelta(days=max_days)).isoformat()

        borrowed[book_id] = {
            "title": book.get("title", ""),
            "borrowed_date": today.isoformat(),
            "due_date": due_date
        }

        patron['borrowed_books'] = json.dumps(borrowed)

        book['Status'] = 'Checked Out'
        book['Checkouts'] = str(int(book.get('Checkouts') or 0) + 1)

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=book_fields)
            writer.writeheader()
            writer.writerows(books)
        shutil.move(tmp, BOOKS_PATH)

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(patrons)
        shutil.move(tmp, patron_path)

        log_transaction("lend", actor_username=current_user.username, patron_library_number=f"{patron['name']} - {lib_no}", bookID=book_id, amount=None, note=f"Lent {book['title']}", path=TRANSACTIONS_PATH)

        blprint("✓ Book lent successfully.")


    def receive_book(self):
        import csv, json, tempfile, shutil, os

        clear_screen()
        print("Receive Returned Book")

        book_id = input(f"{GREEN}Enter Book ID:{RESET} ").strip()
        if not book_id:
            return

        with open(BOOKS_PATH, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            books = list(reader)
            fields = reader.fieldnames

        book = next((b for b in books if (b.get('bookID') or '').strip() == book_id), None)
        if not book:
            print("Book not found.")
            return

        book['Status'] = 'Available'

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(books)
        shutil.move(tmp, BOOKS_PATH)

        patron_path = 'patron1.csv'
        with open(patron_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            patrons = list(reader)
            p_fields = reader.fieldnames

        for p in patrons:
            try:
                borrowed = json.loads(p.get('borrowed_books') or '{}')
            except Exception:
                borrowed = {}

            if book_id in borrowed:
                del borrowed[book_id]
                p['borrowed_books'] = json.dumps(borrowed)

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=p_fields)
            writer.writeheader()
            writer.writerows(patrons)
        shutil.move(tmp, patron_path)

        log_transaction("receive", actor_username=current_user.username, patron_library_number=None, bookID=book_id, amount=None, note=f"Returned {book['title']}", path=TRANSACTIONS_PATH)

        blprint("✓ Book returned successfully.")

    def edit_book_status(self):
        import tempfile, os, csv, shutil
        clear_screen()
        print("Edit Book Status")
        
        book_id = input(f"{GREEN}Enter Book ID to edit (or B to cancel):{RESET} ").strip()
        if not book_id or book_id.lower() == 'b':
            blprint("Aborted.")
            return

        books_path = 'books123.updated.csv'
        if not os.path.exists(books_path):
            print("Books file not found.")
            return

        with open(books_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            books_rows = list(reader)

        book = None
        for row in books_rows:
            if (row.get('bookID') or '').strip() == book_id:
                book = row
                break

        if not book:
            print(f"Book ID {book_id} not found.")
            return

        current_status = (book.get('Status') or '').strip()
        print(f"\nCurrent Book Details:")
        print(f"  Title: {book.get('title', '')}")
        print(f"  Current Status: {current_status}")
        print(f"  Checkouts: {book.get('Checkouts', '0')}")

        print("\nSelect New Status:")
        print("1. Available")
        print("2. Checked Out")
        print("3. Reserved")
        print("4. Lost")

        choice = input(f"{GREEN}Enter your choice (1-4) or B to cancel:{RESET} ").strip()
        if choice.lower() == 'b':
            blprint("Aborted.")
            return

        status_of_book = {
            '1': 'Available',
            '2': 'Checked Out',
            '3': 'Reserved',
            '4': 'Lost'
        }

        if choice not in status_of_book:
            rprint("Invalid choice.")
            return

        new_status = status_of_book[choice]

        book['Status'] = new_status

        fd, tmp_path = tempfile.mkstemp(prefix='books_', suffix='.csv', dir='.')
        os.close(fd)

        with open(tmp_path, mode='w', newline='', encoding='utf-8') as out:
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            sanitized_rows = []
            for row in books_rows:
                clean_row = {fn: (row.get(fn, '') if row.get(fn) is not None else '') for fn in fieldnames}
                sanitized_rows.append(clean_row)
            writer.writerows(sanitized_rows)

        shutil.move(tmp_path, books_path)

        blprint(f"\n✓ Book ID {book_id} status updated from '{current_status}' to '{new_status}'.")
    
    def receive_fines_from_patron(self):
        import csv, tempfile, shutil, os

        global _fines_collected  

        clear_screen()
        print("Receive Fines From Patron")

        lib_no = input(f"{GREEN}Enter patron library number (or B to cancel):{RESET} ").strip()
        if not lib_no or lib_no.lower() == 'b':
            return

        patron_path = 'patron1.csv'
        with open(patron_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            patrons = list(reader)
            fieldnames = reader.fieldnames

        patron = next((p for p in patrons if p.get('library_number') == lib_no), None)
        if not patron:
            rprint("Patron not found.")
            return

        try:
            current_fines = float(patron.get('fines') or 0)
        except ValueError:
            current_fines = 0.0

        blprint(f"Current fines: ₱{current_fines:.2f}")

        try:
            payment = float(input(f"{GREEN}Enter payment amount:{RESET} ").strip())
        except ValueError:
            rprint("Invalid payment.")
            return

        if payment <= 0:
            rprint("Payment must be positive.")
            return

        if payment > current_fines:
            rprint("Payment exceeds outstanding fines.")
            return

        patron['fines'] = f"{current_fines - payment:.2f}"

        
        _fines_collected += payment

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(patrons)
        shutil.move(tmp, patron_path)

        log_transaction("fine_payment", actor_username=current_user.username, patron_library_number=f"{patron['name']} - {patron['library_number']}", bookID=None, amount=payment, note="Fine payment received", path=TRANSACTIONS_PATH)
        blprint(f"✓ Payment of ₱{payment:.2f} received successfully.")


    def view_transactions(self):
        clear_screen()
        bprint("Recent Transactions")
        try:
            recent = view_transactions(100)
        except Exception:
            print("Could not read transactions file.")
            return
        if not recent:
            print("No transactions recorded yet.")
            return
        patron_map = {}
        try:
            with open('patron1.csv', mode='r', newline='', encoding='utf-8') as pfile:
                preader = csv.DictReader(pfile)
                for pr in preader:
                    key = (pr.get('library_number') or '').strip()
                    if key:
                        patron_map[key] = pr.get('name', '').strip()
        except Exception:
            patron_map = {}

        staff_map = {}
        try:
            with open('librarian1.csv', mode='r', newline='', encoding='utf-8') as lfile:
                lreader = csv.DictReader(lfile)
                for lr in lreader:
                    username = (lr.get('username') or '').strip()
                    name = (lr.get('name') or '').strip()
                    if username and name:
                        staff_map[username] = {'name': name, 'type': 'librarian'}
        except Exception:
            pass

        try:
            with open('assistant1.csv', mode='r', newline='', encoding='utf-8') as afile:
                areader = csv.DictReader(afile)
                for ar in areader:
                    username = (ar.get('username') or '').strip()
                    name = (ar.get('name') or '').strip()
                    if username and name:
                        staff_map[username] = {'name': name, 'type': 'assistant'}
        except Exception:
            pass

        cols = [
            ('timestamp', 10),  
            ('type', 12),
            ('actor', 12),
            ('patron', 24),
            ('bookID', 8),
            ('amount', 10),
            ('note', 40),
        ]

        rows = []
        for t in recent:
            ts_raw = t.get('timestamp','')
            ts = ''
            if ts_raw:
                try:
                    ts = datetime.datetime.fromisoformat(ts_raw).date().isoformat()
                except Exception:
                    ts = ts_raw[:10]

            ttype = (t.get('type','') or '')
            actor_username = (t.get('actor_username','') or '').strip()
            
            if actor_username and actor_username in staff_map:
                staff_info = staff_map[actor_username]
                actor_name = staff_info['name']
                if current_user and current_user.username == actor_username:
                    actor = f"{actor_name}(You)"
                elif staff_info['type'] == 'assistant':
                    actor = f"{actor_name}(Assistant)"
                else:
                    actor = f"{actor_name}(Librarian)"
            else:
                actor = actor_username or ''
            
            patron_key = (t.get('patron_library_number','') or '').strip()
            if patron_key and patron_key in patron_map:
                patron_display = f"{patron_map[patron_key]}({patron_key})"
            else:
                patron_display = patron_key or ''
            bookid = (t.get('bookID','') or '')
            amount = (t.get('amount','') or '')
            note = (t.get('note','') or '')
            rows.append((ts, ttype, actor, patron_display, bookid, amount, note))

        widths = []
        for i, (name, maxw) in enumerate(cols):
            header_len = len(name)
            content_max = max((len(str(r[i])) for r in rows), default=0)
            w = min(max(header_len, content_max), maxw)
            widths.append(w)

        header = ' | '.join(name.ljust(widths[i]) for i, (name, _) in enumerate(cols))
        sep = '-+-'.join('-' * widths[i] for i in range(len(cols)))
        print(header)
        print(sep)

        for r in rows:
            out = []
            for i, cell in enumerate(r):
                s = str(cell)
                w = widths[i]
                if len(s) > w:
                    s = s[:max(0, w-3)] + '...'
                out.append(s.ljust(w))
            print(' | '.join(out))

    def report(self):
        generate_library_report()
    
    @classmethod
    def show_patrons_info(cls):
        import csv, json

        headers = [
            'Name', 'Age', 'Library no.', 'Fines', 'Days Overdue',
            'Max Books', 'Max Days', 'Contact', 'Preferences', 'Borrowed Books'
        ]

        with open('patron1.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            patrons = list(reader)

        rows = []
        for p in patrons:
            try:
                borrowed = json.loads(p.get('borrowed_books') or '{}')
            except Exception:
                borrowed = {}

            
            borrowed_text = "\n".join(
                f"{bid} - {(info.get('title','')[:20] + '...') if len(info.get('title','')) > 20 else info.get('title','')}"
                for bid, info in borrowed.items()
            )

            obj = p.get('object') or ''
            ptype = ''
            if obj and '(' in obj:
                ptype = obj.split('(')[0]
            elif obj:
                ptype = obj
            display_name = f"{p.get('name','')}({ptype})" if ptype else p.get('name','')

            rows.append([
                display_name,
                p.get('age', ''),
                p.get('library_number', ''),
                p.get('fines', ''),
                p.get('days_overdue', ''),
                p.get('max_books_allowed', ''),
                p.get('max_days_allowed', ''),
                p.get('contact_number', ''),
                p.get('book_preferences', ''),
                borrowed_text
            ])

        widths = [
            max(len(headers[i]), max((len(line) for r in rows for line in str(r[i]).split("\n")), default=0))
            for i in range(len(headers))
        ]

        bprint("  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
        bprint("  ".join("-" * widths[i] for i in range(len(headers))))

        for r in rows:
            lines = [str(c).split("\n") for c in r]
            for i in range(max(len(l) for l in lines)):
                print("  ".join((lines[c][i] if i < len(lines[c]) else "").ljust(widths[c])
                                for c in range(len(headers))))
            print()


    def edit_patron_info(self):
        import tempfile, shutil
        clear_screen()
        print("Edit Patron Information")

        lib_input = input(f"{GREEN}Enter patron library number (or B to cancel):{RESET} ").strip()
        if not lib_input or lib_input.lower() == 'b':
            blprint("Aborted.")
            return

        try:
            library_number = int(lib_input)
        except ValueError:
            rprint("Invalid library number.")
            return

        patron_path = 'patron1.csv'
        if not os.path.exists(patron_path):
            print("Patron file not found.")
            return

        with open(patron_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            raw_fieldnames = reader.fieldnames or []
            fieldnames = [fn for fn in raw_fieldnames if fn and str(fn).strip()]
            patrons = list(reader)

        patron = None
        for p in patrons:
            try:
                if int(p.get('library_number', -1)) == library_number:
                    patron = p
                    break
            except ValueError:
                continue

        if not patron:
            rprint(f"No patron ID {library_number} found.")
            return

        clear_screen()
        print(f"Patron: {patron.get('name', '')}")
        print(f"Library Number: {library_number}\n")
        bprint("Current Information:")
        print(f"  Age: {patron.get('age', '')}")
        print(f"  Contact: {patron.get('contact_number', '')}")
        print(f"  Preferences: {patron.get('book_preferences', '')}")
        print(f"  Max Books: {patron.get('max_books_allowed', '')}")
        print(f"  Max Days: {patron.get('max_days_allowed', '')}\n")

        while True:
            bprint("Edit Options:")
            print("1. Name")
            print("2. Age")
            print("3. Contact Number")
            print("4. Book Preferences")
            print("5. Max Books Allowed")
            print("6. Max Days Allowed")
            print("0. Done\n")

            choice = input(f"{GREEN}Enter your choice (0-6):{RESET} ").strip()

            if choice == '0':
                break
            elif choice == '1':
                new_name = input(f"{GREEN}Enter new name:{RESET} ").strip()
                if new_name:
                    patron['name'] = new_name
                    blprint("✓ Name updated.")
            elif choice == '2':
                try:
                    new_age = int(input(f"{GREEN}Enter new age:{RESET} ").strip())
                    if new_age >= 0:
                        patron['age'] = str(new_age)
                        blprint("✓ Age updated.")
                    else:
                        print("Age cannot be negative.")
                except ValueError:
                    rprint("Invalid age.")
            elif choice == '3':
                new_contact = input(f"{GREEN}Enter new contact number:{RESET} ").strip()
                patron['contact_number'] = new_contact
                blprint("✓ Contact updated.")
            elif choice == '4':
                new_prefs = input(f"{GREEN}Enter new book preferences:{RESET} ").strip()
                patron['book_preferences'] = new_prefs
                blprint("✓ Preferences updated.")
            elif choice == '5':
                try:
                    new_max = int(input(f"{GREEN}Enter new max books allowed:{RESET} ").strip())
                    if new_max >= 0:
                        patron['max_books_allowed'] = str(new_max)
                        blprint("✓ Max books updated.")
                    else:
                        print("Max books cannot be negative.")
                except ValueError:
                    rprint("Invalid number.")
            elif choice == '6':
                try:
                    new_days = int(input(f"{GREEN}Enter new max days allowed:{RESET} ").strip())
                    if new_days >= 0:
                        patron['max_days_allowed'] = str(new_days)
                        blprint("✓ Max days updated.")
                    else:
                        print("Max days cannot be negative.")
                except ValueError:
                    rprint("Invalid number.")
            else:
                rprint("Invalid choice.")
            print()

        fd, tmp_path = tempfile.mkstemp(prefix='patrons_', suffix='.csv', dir='.')
        os.close(fd)
        try:
            with open(tmp_path, mode='w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()
                sanitized_patrons = []
                for p in patrons:
                    clean_patron = {fn: (p.get(fn, '') if p.get(fn) is not None else '') for fn in fieldnames}
                    sanitized_patrons.append(clean_patron)
                writer.writerows(sanitized_patrons)
            shutil.move(tmp_path, patron_path)
            blprint(f"✓ Patron information updated successfully.")
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass
    

def _input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        rprint("This field is required. Please enter a value.")


class Librarian(Staff):
    def __repr__(self):
        return f'Librarian({self.name}, {self.age}, {self.username})'
    @classmethod
    def add_librarian(cls):
        clear_screen()
        print('=' * 40)
        bprint('Welcome to the library management system!')
        print('Since this is your first time, please create a librarian account to get started.')
        print('=' * 40)
        print('')
        name = _input_non_empty(f"{GREEN}Enter librarian's name:{RESET} ")
        while True:
            try:
                age = int(input(f"{GREEN}Enter librarian's age:{RESET} "))
                if age < 0:
                    rprint("Age cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                rprint("Please enter a valid integer for age.")

        while True:
            username = _input_non_empty(f"{GREEN}Enter librarian's username:{RESET} ")
            with open('librarian1.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                if any(row['username'] == username for row in reader):
                    rprint("Username already exists. Please choose a different username.\n")
                else:
                    break
        password = _input_non_empty(f"{GREEN}Enter librarian's password:{RESET} ")
        new_librarian = Librarian(name, age, username, password)
        library_number = generate_library_number()
        obj = repr(new_librarian)
        fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
        needs_header = not os.path.exists('librarian1.csv') or os.path.getsize('librarian1.csv') == 0
        with open('librarian1.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if needs_header:
                writer.writeheader()
            writer.writerow({'name': name, 'age': age, 'username': username, 'password': password, 'library_number': library_number, 'object': obj})
    

    def add_assistant(self): 
        name = _input_non_empty(f"{GREEN}Enter assistant's name:{RESET} ")
        
        while True:
            try:
                age = int(input(f"{GREEN}Enter assistant's age:{RESET} "))
                if age < 0:
                    rprint("Age cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                rprint("Please enter a valid integer for age.")
        
        while True:
            username = _input_non_empty(f"{GREEN}Enter assistant's username:{RESET} ")
            with open('assistant1.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                if any(row['username'] == username for row in reader):
                    rprint("Username already exists. Please choose a different username.\n")
                else:
                    break
        password = _input_non_empty(f"{GREEN}Enter assistant's password:{RESET} ")
        new_assistant = Assistant(name, age, username, password)
        library_number = generate_library_number()
        obj = repr(new_assistant)
        fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
        needs_header = not os.path.exists('assistant1.csv') or os.path.getsize('assistant1.csv') == 0
        with open('assistant1.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if needs_header:
                writer.writeheader()
            writer.writerow({'name': name, 'age': age, 'username': username, 'password': password, 'library_number': library_number, 'object': obj})
        
        blprint(f"Assistant '{username}' has been successfully created.") 
        

    def remove_assistant(self):
       clear_screen()
       self.show_assistants_info()
       username = input(f"{GREEN}Enter the username of the assistant to remove/Press B to go cancel:{RESET} ")
       if username.lower() == 'b':
        return
       with open('assistant1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            assistants = list(reader)
       with open('assistant1.csv', mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'username', 'password', 'library_number', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            removed = False
            for assistant in assistants:
                if assistant['username'] != username:
                    writer.writerow(assistant)
                else:
                    removed = True
        
            if removed:
                blprint(f'Assistant with username {username} removed successfully.')
            else:
                rprint(f'Assistant with username {username} not found.')
    
    
    def show_assistants_info(self):
        clear_screen()
        with open('assistant1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            assistants = list(reader)
            if not assistants:
                print("No assistants available.")
                return

            name_w = max(len('Name'), max((len(str(a.get('name',''))) for a in assistants), default=0))
            age_w = max(len('Age'), max((len(str(a.get('age',''))) for a in assistants), default=0))
            user_w = max(len('Username'), max((len(str(a.get('username',''))) for a in assistants), default=0))
            pass_w = max(len('Password'), max((len(str(a.get('password',''))) for a in assistants), default=0))

            bprint(f"{ 'Name'.ljust(name_w) }  { 'Age'.ljust(age_w) }  { 'Username'.ljust(user_w) }  { 'Password'.ljust(pass_w) }")
            print(f"{ '-'*name_w }  { '-'*age_w }  { '-'*user_w }  { '-'*pass_w }")

            for assistant in assistants:
                print(f"{ str(assistant.get('name','')).ljust(name_w) }  { str(assistant.get('age','')).ljust(age_w) }  { str(assistant.get('username','')).ljust(user_w) }  { str(assistant.get('password','')).ljust(pass_w) }")


    def add_patron(self):
        while True:
         choice=input(f"{GREEN}Enter your choice: {RESET}")
         if choice.isdigit() and 1 <= int(choice) <= 4:
                break
         else:
                rprint("Invalid choice. Please enter a number between 1 and 4.")
        name = _input_non_empty(f"{GREEN}Enter patron's name:{RESET} ")
        while True:
         try:
          age = int(input(f"{GREEN}Enter patron's age:{RESET} "))
          if age < 0:
            print("Age cannot be negative.")
            continue
          break
         except ValueError:
          rprint("Please enter a valid integer for age.")
        library_number = generate_library_number()
        if choice == "1":  
            new_patron = Student(name, age, library_number)
            blprint(f'Student added with library number: {library_number}')
        elif choice == "2": 
            new_patron = Faculty(name, age, library_number)
            blprint(f'Faculty added with library number: {library_number}')
        elif choice == "3": 
            new_patron = Community(name, age, library_number)
            blprint(f'Community member added with library number: {library_number}')
        elif choice == "4":
            while age > 12:
                rprint("Age exceeds the limit for Child patron type.")
                try:
                    childd = int(input(f"{GREEN}Enter a valid age (12 or below):{RESET} ").strip())
                except ValueError:
                    rprint("Please enter a valid integer for age.")
                    age = 13
                    continue
                age = childd
            new_patron = Child(name, age, library_number)
            blprint(f'Child added with library number: {library_number}')
        contact_number = input(f"{GREEN}Enter contact number(optional):{RESET} ").strip()
        book_preferences = input(f"{GREEN}Enter book preferences:(optional) {RESET}").strip()

        corrector()
        fieldnames = [
            'name', 'age', 'library_number', 'fines',
            'days_overdue', 'max_books_allowed', 'max_days_allowed',
            'contact_number', 'book_preferences', 'borrowed_books', 'object'
        ]
        with open('patron1.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({
                'name': new_patron.name,
                'age': new_patron.age,
                'library_number': new_patron.library_number,
                'fines': new_patron.fines,
                'days_overdue': new_patron.days_overdue,
                'max_books_allowed': new_patron.max_books_allowed,
                'max_days_allowed': new_patron.max_days_allowed,
                'contact_number': contact_number,
                'book_preferences': book_preferences,
                'borrowed_books': new_patron.borrowed_books,
                'object': repr(new_patron)
            })
        
    def remove_patron(self):
        clear_screen()
        current_user.show_patrons_info()
        lib_input = input(f"{GREEN}Enter the library number of the patron to remove/Press B to cancel:{RESET} ")
        if lib_input.lower() == 'b':
            return
        try:
            library_number = int(lib_input)
        except ValueError:
            rprint("Invalid library number. Please enter a numeric value.")
            return

        
        with open('patron1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            patrons = list(reader)

        if not any(int(p.get('library_number', -1)) == library_number for p in patrons):
            rprint('Library number does not exist.')
            return

        with open('patron1.csv', mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'library_number', 'fines',
                          'days_overdue', 'max_books_allowed', 'max_days_allowed',
                          'contact_number', 'book_preferences', 'borrowed_books', 'object']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            removed = False
            for patron in patrons:
                if int(patron['library_number']) != library_number:
                    writer.writerow(patron)
                else:
                    removed = True

        if removed:
            used_library_numbers.discard(library_number)
            blprint(f'Patron with library number {library_number} removed successfully.')
        else:
            print(f'Patron with library number {library_number} not found.')



class Assistant(Staff):
 def __repr__(self):
        return f'Assistant({self.name}, {self.age}, {self.username})'
class Patron(Person):
    def __init__(self, name, age,library_number, fines=0.0 ,borrowed_books=None,days_overdue=0, max_books_allowed=0, max_days_allowed=0):
        super().__init__(name, age)
        self.fines=fines
        self.borrowed_books=borrowed_books if borrowed_books is not None else {}
        self.days_overdue=days_overdue
        self.max_books_allowed=max_books_allowed
        self.max_days_allowed=max_days_allowed
        self.library_number=library_number
    def __repr__(self):
        return f'Patron({self.name}, {self.age}, {self.library_number})'
    
class Student(Patron):
     def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=5, max_days_allowed=30)
     def __repr__(self):
        return f'Student({self.name},{self.age})'
class Faculty(Patron):
     def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=10, max_days_allowed=60)
     def __repr__(self):
        return f'Faculty({self.name},{self.age})'
    

class Community(Patron):
    def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=3, max_days_allowed=20)
    def __repr__(self):
        return f'Community({self.name},{self.age})'

class Child(Patron):
    def __init__(self, name, age, library_number):
        super().__init__(name, age, library_number, max_books_allowed=2, max_days_allowed=15)
    def __repr__(self):
        return f'Child({self.name},{self.age})'

class Report:
    def __init__(self, title, date=None):
        self.title = title
        self.date = date if date is not None else datetime.date.today()
        self.contents = []

    def add_content(self, content):
        self.contents.append(content)

    def generate(self):
        body = []
        for s in self.contents:
            body.append(s.generate())
        return "\n".join(body)


class Reports:
    def __init__(self, name):
        self.name = name

    def generate(self):
        pass  

class Inventory(Reports):
    def __init__(self, books=BOOKS_PATH):
        super().__init__('Inventory Summary')
        self.books = BOOKS_PATH
  

    def generate(self):
        rows = read(self.books)
        total = len(rows)

        circulated = sum(1 for r in rows if to_int((r.get('Checkouts') or 0)) > 0)
        circulation_rate = round((circulated / total) * 100, 2) if total > 0 else 0.0

        ages = []
        current_year = datetime.date.today().year
        for r in rows:
            try:
                year = int(r.get('publication_year') or 0)
                ages.append(current_year - year)
            except Exception:
                continue

        average_age = round(sum(ages) / len(ages), 2) if ages else 0.0
        weeding = sum(1 for i in ages if i > 10)

        return (f"Inventory Summary:\n"
                f"Total Books: {total}\n"
                f"Circulation Rate: {circulation_rate}%\n"
                f"Average Book Age: {average_age} years\n"
                f"Books Eligible for Weeding (>10 years): {weeding}\n")

class Circulation(Reports):
    def __init__(self, transactions=TRANSACTIONS_PATH, books=BOOKS_PATH):
        super().__init__('Circulation Activity')
        self.transactions = transactions
        self.books = books

    def generate(self):
        import re
        
        global BOOKS_PATH
        rows = read(BOOKS_PATH)
        
        if not rows:
            return "Circulation Activity:\nTotal Checkouts: 0\nMost Checked Out Book: N/A"
        
        total_checkouts = 0
        safe_rows = []
        
        for r in rows:
            checkout_value = r.get('Checkouts', '0')
            
            try:
                cleaned_value = str(checkout_value).strip()
                current_checkouts = int(cleaned_value)
                total_checkouts += current_checkouts
                
                r['Checkouts_INT'] = current_checkouts
                safe_rows.append(r)
            except ValueError:
                continue

        most_checked_out = max(
            safe_rows, 
            key=lambda r: r['Checkouts_INT'], 
            default=None
        )
        
        if most_checked_out:
            title = most_checked_out.get('title', 'N/A')
            count = most_checked_out.get('Checkouts', '0')
            most_checked_out_info = f"Most Checked Out Book: {title} (Checkouts: {count})"
        else:
            most_checked_out_info = "Most Checked Out Book: N/A (No valid checkout data)"


        return (f"Circulation Activity:\n"
                f"Total Checkouts: {total_checkouts}\n"
                f"{most_checked_out_info}\n")
    
class PatronReport(Reports):
    def __init__(self, patrons=PATRONS_PATH):
        super().__init__('Patron Report')
        self.patrons = patrons

    def generate(self):
        rows = read(self.patrons)
        
        active_patrons = 0
        total_items = 0

        for r in rows:
            try:
                borrowed = json.loads(r.get('borrowed_books') or '{}')
                if borrowed:
                    active_patrons += 1
                    total_items += len(borrowed)
            except Exception:
                continue
    
        average_items = round(total_items / active_patrons, 2) if active_patrons > 0 else 0.0

        return (f"Patron Report:\n"
                f"Active Patrons: {active_patrons}\n"
                f"Average Items Borrowed per Active Patron: {average_items}\n")
    
class Finance(Reports):
    def __init__(self, patrons=PATRONS_PATH):
        super().__init__('Financial Report')
        self.patrons = patrons

    def generate(self):
        rows = read(self.patrons)
        
        total_fines = 0.0

        for r in rows:
            try:
                fines = float(r.get('fines') or 0.0)
                total_fines += fines
            except Exception:
                continue

        return (f"Financial Report:\n"
                f"Total Outstanding Fines: PHP{total_fines:.2f}\n")

def first_menu():
    global current_user
    bprint("Welcome to the Library Management System")
    print("Since there is no accounts yet, please create your librarian account to get started.")
    Librarian.add_librarian()
    with open('librarian1.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            current_user = Librarian(row['name'], int(row['age']), row['username'], row['password'])
            blprint(f"Account created successfully. Welcome, {current_user.name}!")
    enter=input(f"{GREEN}\nPress Enter to continue to the menu.{RESET}")
    clear_screen()
    librarian_menu()
    
def read(path):
    if not os.path.exists(path):
        return []
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)           

def generate_library_report():
    report = Report("Sample Library Report", "January 2024")
    report.add_content(Circulation())
    report.add_content(PatronReport())
    report.add_content(Inventory())
    report.add_content(Finance())
    bprint("\n" + report.generate())

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def login_menu():
    global current_user
    print('================================')
    print(f"{BOLD}Welcome to the Library Management System{RESET}")
    print('================================')

    print("Please log in to continue.")
    print("1. Librarian Login")
    print("2. Assistant Login")
    print("3. Exit")
    print("4. Forgot Password(FOR LIBRARIAN ONLY, REFER TO VIDEO DEMO)\n\n")
    print(f"{BOLD}NOTE: If you are an assistant and YOU DONT HAVE ACCOUNT OR FORGOT PASSWORD, please contact the librarian.{RESET}")
    while True:
        choice=input(f"{GREEN}Enter your choice (1-4): {RESET}").strip()
        
        if not choice:
            continue
        if choice.lower() == 'b':
            clear_screen()
            starting_point()
            return
        if choice in ['1', '2', '3','4']:
            break
        else:
            rprint("Invalid choice. Please enter a number between 1 and 4 or 'B' to go back.")
    while True:
     if choice == '1':
        username = input(f"{GREEN}Enter your username: {RESET}")
        password = input(f"{GREEN}Enter your password: {RESET}")
        with open('librarian1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    current_user = Librarian(row['name'], int(row['age']), row['username'], row['password'])
                    blprint(f"Login successful. Welcome, {current_user.name}!")
                    
                    librarian_menu()
                    return
            rprint("Invalid username or password.\n")
            retry = input(f"{GREEN}{BOLD}PRESS ENTER TO TRY AGAIN OR 'B' TO GO BACK TO LOGIN CHOICE:{RESET} \n").strip().lower()
            if retry == 'b':
                clear_screen()
                login_menu()
                return
            
     elif choice == '2':
        username = input(f"{GREEN}Enter your username: {RESET}")
        password = input(f"{GREEN}Enter your password: {RESET}")
        with open('assistant1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    current_user = Assistant(row['name'], int(row['age']), row['username'], row['password'])
                    blprint(f"Login successful. Welcome, {current_user.name}!")
                    
                    assistant_menu()
                    return
            rprint("Invalid username or password.\n")
            retry = input(f"{GREEN} Press Enter to try again or 'B' TO GO BACK TO LOGIN CHOICE:{RESET} \n").strip().lower()
            if retry == 'b':
                clear_screen()
                login_menu()
                return
            
     elif choice == '3':
        blprint("Exiting the system. Goodbye!")
        exit()
     elif choice == '4':
       sikretong_password="eee111"
       secret_password=input(f"{GREEN}What's the secret password(REFER TO VIDEO DEMO): {RESET}")
       if secret_password.lower()==sikretong_password.lower():
         with open('librarian1.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                oprint(f"{BOLD}The Librarian Username is: {row['username']}; Password is: {row['password']}{RESET}")
            enter=input(f"{GREEN}\nPress Enter to return to the login menu.{RESET}")
            clear_screen()
            login_menu()
            return
       else:
            rprint("Incorrect secret password. REFER TO VIDEO DEMO\n")
            enter=input(f"{GREEN}\nPress Enter to return to the login menu.{RESET}")
            clear_screen()
            login_menu()
            return


def librarian_menu():
    global current_user, current_client
    
    while True:
     clear_screen()
     bprint("Welcome to the Library Management System")
     bprint("\n====== Librarian Menu ======\n")
     print("1. Add Book")
     print("2. Remove Book")
     print('3. Lend Book/Receive Book/Edit book status')
     print("4. Show Patron Info")
     print('5. Receive fines from Patron')
     print("6. Add Assistant")
     print("7. Show Assistants")
     print("8. Remove Assistant")
     print("9. Add Patron")
     print("10. Remove Patron")
     print("11. Edit Patron Info")
     print('12. Show transaction history')
     print("13. Calculate Overall Fines")
     print("14. Generate Report")
     print('15. Search Books')
     print("16. Logout")
     print('17. Change password')
     print("0. Exit\n")
     while True:
        next_choice=input(f"{GREEN}Enter your choice: {RESET}")
        if next_choice.isdigit() and 0 <= int(next_choice) <= 17:
            break
        else:
            rprint("Invalid choice. Please enter a number between 0 and 17.")
     if next_choice=='1': 
        clear_screen()
        current_user.add_book()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='2':
        clear_screen()
        current_user.remove_book()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='3':
        clear_screen()
        print("1. Lend Book")
        print("2. Receive Book")
        print("3. Edit Book Status")
        while True:
         choice=input(f"{GREEN}Enter your choice: {RESET}")
         if choice.isdigit() and 1 <= int(choice) <= 3:
                break
         else:
                rprint("Invalid choice. Please enter a number between 1 and 3.")
        if choice=='1':
            current_user.lend_book()
            enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
            clear_screen()
            continue
        if choice=='2':
            current_user.receive_book()
            enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
            clear_screen()
            continue
        if choice=='3':
            clear_screen()
            menu6_1()
            current_user.edit_book_status()
            enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
            clear_screen()
            continue
     if next_choice=='4':
        clear_screen()
        current_user.show_patrons_info()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='5':
        clear_screen()
        current_user.receive_fines_from_patron()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='6':
        clear_screen()
        current_user.add_assistant()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='7':
        clear_screen()
        current_user.show_assistants_info()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='8':
        clear_screen()
        current_user.remove_assistant()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue

     if next_choice=='9':
        clear_screen()
        menu_10_1()
        current_user.add_patron()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='10':
        clear_screen()
        current_user.remove_patron()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='11':
        current_user.edit_patron_info()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='12':
        clear_screen()
        try:
            current_user.view_transactions()
        except Exception:
            print("Could not load transactions.")
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='13':
        clear_screen()
        current_user.calculate_overdue_fines()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='14':
        clear_screen()
        generate_library_report()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='15':
        clear_screen()
        current_user.search_book()
        clear_screen()
        continue
     if next_choice=='16':
       clear_screen()
       current_user=None
       clear_screen()
       login_menu()
       break

     if next_choice=='17':
        clear_screen()
        current_user.change_password()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='0':
        blprint("Thank you for using the Library Management System. Goodbye!")
        exit()

    
def assistant_menu():
    global current_user, current_client
    
    while True:
     clear_screen()
     bprint("Welcome to the Library Management System")
     bprint("\n====== Assistant Menu ======\n")
     print("1. Add Book")
     print("2. Remove Book")
     print("3. Lend Book/Receive Book/Edit book status")
     print("4. Show Patron Info")
     print("5. Receive fines from Patron")
     print("6. Search Books")
     print("7. Logout")
     print("0. Exit\n")
     while True:
      next_choice=input(f"{GREEN}Enter your choice:{RESET} ")
      if next_choice.isdigit() and 0 <= int(next_choice) <= 7:
                break
      else:
                rprint("Invalid choice. Please enter a number between 0 and 7.")
                continue
     if next_choice=='1': 
        clear_screen()
        current_user.add_book()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='2':
        clear_screen()
        current_user.remove_book()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='3':
        clear_screen()
        print("1. Lend Book")
        print("2. Receive Book")
        print("3. Edit Book Status")
        while True:
         choice=input(f"{GREEN}Enter your choice:{RESET} ")
         if choice.isdigit() and 1 <= int(choice) <= 3:
                break
         else:
                rprint("Invalid choice. Please enter a number between 1 and 3.")
        if choice=='1':
            current_user.lend_book()
            enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
            clear_screen()
            continue
        if choice=='2':
            current_user.receive_book()
            enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
            clear_screen()
            continue
        if choice=='3':
            clear_screen()
            menu6_1()
            current_user.edit_book_status()
            enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
            clear_screen()
            continue
     if next_choice=='4':
        clear_screen()
        current_user.show_patrons_info()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='5':
        clear_screen()
        current_user.receive_fines_from_patron()
        enter=input(f"{GREEN}\nPress Enter to return to the menu.{RESET}")
        clear_screen()
        continue
     if next_choice=='6':
        clear_screen()
        current_user.search_book()
        clear_screen()
        continue
     if next_choice=='7':
         clear_screen()
         current_user=None
         clear_screen()
         login_menu()
         break
    
     if next_choice=='0':
        blprint("Thank you for using the Library Management System. Goodbye!")
        exit()  
def menu_10_1():
    print("Select Patron Type to Add:")
    print("1. Student")
    print("2. Faculty")
    print("3. Community")
    print("4. Child") 
    
def menu6_1():
    print("Select Book Status to Edit:")
    print("1. Available")
    print("2. Checked Out")
    print("3. Reserved")
    print("4. Lost")

def starting_point():
 with open('librarian1.csv', mode='r', newline='') as file:
    if os.path.getsize('librarian1.csv') == 0 or len(file.readlines()) <= 1:
        first_menu()
    else:
        login_menu()

starting_point()