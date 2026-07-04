class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author

class Member:
    def __init__(self,name,member_id):
        self.name = name
        self.member_id = member_id
        self.books = []
            
    def display_member_info(self):
        print(f"Member Name: {self.name}")
        print(f"Member ID: {self.member_id}")
        if len(self.books) > 0:
            print("Borrowed Books:")
            for book in self.books:
                print(f"{book.title}")
        else:
            print("No books borrowed.")

class Library:
    def __init__(self,name):
        self.name = name
        self.available_books = []
        self.borrowed_books = []
        self.transactions = []
    
    def add_book(self,book):
        self.available_books.append(book)
        print(f"{book.title} by {book.author} added to the library.")

    def remove_book(self,book):
        if book in self.available_books:
            self.available_books.remove(book)
            print(f"{book.title} by {book.author} removed")
        else:
            print("Book not found")

    def borrow_book(self,book,member,date):
        if book in self.available_books:
            self.available_books.remove(book)
            self.borrowed_books.append(book)
            self.transactions.append({
                "member" : member.name,
                "book" : book.title,
                "date" : date,
                "action": "borrowed"
            })
            member.books.append(book)
            print(f"{member.name} borrowed {book.title} on {date}")
        else:
            print("Book not available")

    def return_book(self,book,member,date):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            self.available_books.append(book)
            self.transactions.append({
                "member" : member.name,
                "book" : book.title,
                "date" : date,
                "action": "returned"
            })
            if book in member.books:
                member.books.remove(book)
            else:
                print("Member does not have this book")
            print(f"{member.name} returned {book.title} on {date}")
        else:
            print("Book not found in borrowed books")

        
b = Book("The Great Gatsby","F. Scott Fitzgerald")
m1 = Member("Alice",1)
l = Library("City Library")
l.add_book(b)
