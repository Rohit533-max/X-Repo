class Book:
    def __init__(self,title,author, category,copies: int):
        self.title = title
        self.author = author
        self.category = category
        self.copies = copies

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
        for existing_book in self.available_books:
            if (existing_book.title == book.title and
                existing_book.author == book.author and
                existing_book.category == book.category):
                existing_book.copies += book.copies
                print(f"book : {book.title} \n book copies : {book.copies} ")
                return
        self.available_books.append(book)
        print(f"{book.title} by {book.author} added to the library.")

    def remove_book(self,book):
        for existing_book in self.available_books:
            if existing_book.title == book.title:

                if(existing_book.copies >1):
                    existing_book.copies -=1
                    print("Remaining copies are: ", existing_book.copies)
            self.available_books.remove(book)
            print(f"Book {book.title} is remvoed completely")

    def borrow_book(self,book,member,date):
        if book in self.available_books:
            self.available_books.remove(book)
            self.borrowed_books.append(book)
            member.books.append(book)
            self.transactions.append({
                "member" : member.name,
                "book" : book.title,
                "date" : date,
                "action": "borrowed"
            })
            print(f"{member.name} borrowed {book.title} on {date}")
        else:
            print("Book not available")

    def return_book(self,book,member,date):
        if book in self.borrowed_books and book in member.books:
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

    def display_available_books(self):
        if self.available_books:
            print("Available books: ")
            for book in self.available_books:
                print(f"{book.title} by {book.author} copies: {book.copies} ({book.category})")
        else:
            print("No books available!")
    def display_borrowed_books(self):
        if self.borrowed_books:
            print("Borrowed books: ")
            for book in self.borrowed_books:
                print(f"{book.title} by {book.author} copies: {book.copies} ({book.category})")
    def transaction_history(self):
        if self.transactions:
            print("Transactions are : ")
            for transaction in self.transactions:
                print(f"{transaction['member']} "
                      f"{transaction['book']} "
                      f"{transaction['date']} "
                      f"{transaction['action']} ")
                
    def get_books_by_category(self,category):
        books = [book for book in self.available_books if book.category.lower() == category.lower()]

        if books:
            for book in books:
                print(f"{book.title} by {book.author}")
        else:
            print(f"No books of category: {category} if available")


#book copies remains to update

# book1 = Book("Python Programming", "John Smith", "Programming",2)
# book2 = Book("Data Science", "Alice Brown", "Technology",1)
# book3 = Book("Applied Matametics", "Ramanujan", "Maths",1)

# member1 = Member("Ali", 101)

# library = Library("City Library")

# library.add_book(book1)
# library.add_book(book2)
# library.add_book(book3)

# # library.display_available_books()

# # library.borrow_book(book1, member1, "07-07-2026")

# # member1.display_member_info()

# # library.return_book(book1, member1, "10-07-2026")

# # library.transaction_history()

# library.get_books_by_category("Maths")