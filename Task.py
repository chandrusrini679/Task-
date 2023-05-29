from datetime import datetime
import requests

API_URL = "https://frappe.io/api/method/frappe-library"


class Books:
    def __init__(self, book_id, title, authors, quantity):
        self.book_id = book_id
        self.title = title
        self.authors = authors
        self.quantity = quantity


class Members:
    def __init__(self, member_id, name, outstanding_debt):
        self.member_id = member_id
        self.name = name
        self.outstanding_debt = outstanding_debt


class Transactions:
    def __init__(self, book, member):
        self.book = book
        self.member = member
        self.issue_date = None
        self.return_date = None
        self.fee_charged = False


class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.transactions = []

    def import_books(self, page=1, title=None, authors=None, isbn=None, publisher=None, num_pages=None):
        params = {
            "page": page,
            "title": title,
            "authors": authors,
            "isbn": isbn,
            "publisher": publisher,
            "num_pages": num_pages
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            books_data = response.json().get("message", [])
            for book_data in books_data:
                book = Books(
                    book_id=book_data["bookID"],
                    title=book_data["title"],
                    authors=book_data["authors"],
                    quantity=0  # Set initial quantity to 0
                )
                self.books.append(book)
        else:
            print("Error: Failed to import books from the API.")

    def search_book(self, keyword):
        results = []
        for book in self.books:
            if keyword.lower() in book.title.lower() or keyword.lower() in book.authors.lower():
                results.append(book)
        return results

    def create_member(self, member_id, name):
        member = Members(member_id=member_id, name=name, outstanding_debt=0)
        self.members.append(member)

    def issue_book(self, book_id, member_id):
        book = self.get_book_by_id(book_id)
        member = self.get_member_by_id(member_id)
        if book and member:
            if book.quantity > 0:
                transaction = Transactions(book=book, member=member)
                transaction.issue_date = datetime.date.today()
                self.transactions.append(transaction)
                book.quantity -= 1
                print("Book issued successfully.")
            else:
                print("Error: Book is out of stock.")
        else:
            print("Error: Invalid book or member ID.")

    def return_book(self, book_id, member_id):
        book = self.get_book_by_id(book_id)
        member = self.get_member_by_id(member_id)
        if book and member:
            transaction = self.get_transaction(book, member)
            if transaction:
                if not transaction.fee_charged:
                    transaction.return_date = datetime.date.today()
                    days_late = (transaction.return_date - transaction.issue_date).days - 15
                    if days_late > 0:
                        fee = days_late * 10  # Assuming fee is Rs. 10 per day
                        member.outstanding_debt += fee
                        if member.outstanding_debt > 500:
                            member.outstanding_debt = 500  # Limit outstanding debt to Rs. 500
                        transaction.fee_charged = True
                        print(f"Book returned successfully. Late fee charged: Rs. {fee}")
                    else:
                        print("Book returned successfully.")
                else:
                    print("Error: Late fee already charged for this transaction.")
            else:
                print("Error: No active transaction found for the book and member.")
        else:
            print("Error: Invalid book or member ID.")

    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def get_member_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def get_transaction(self, book, member):
        for transaction in self.transactions:
            if transaction.book == book and transaction.member == member and not transaction.return_date:
                return transaction
        return None


library = Library()

# Import books from API

library.import_books(page=1, title="Harry Potter", num_books=20)

# Create members

library.create_member(member_id="M001", name="John Doe")
library.create_member(member_id="M002", name=" Smith")

# Issue a book to a member

library.issue_book(book_id="35460", member_id="M001")

# Return a book from a member

library.return_book(book_id="35460", member_id="M001")
