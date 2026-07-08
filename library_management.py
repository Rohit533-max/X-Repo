class Book:

    def __init__(self, title, author, category, copies):
        self.title = title
        self.author = author
        self.category = category
        self.copies = copies

    def display(self):
        return f"{self.title} by {self.author} ({self.category})"



class Member:

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.books = []


    def display_member_info(self):

        print("\nMember Information")
        print("------------------")
        print(f"Name: {self.name}")
        print(f"ID: {self.member_id}")


        if self.books:

            print("Borrowed Books:")

            for book in self.books:
                print(f"- {book.title}")

        else:
            print("No books borrowed.")





class Library:


    def __init__(self, name):

        self.name = name
        self.available_books = []
        self.borrowed_books = []
        self.transactions = []




    def add_book(self, book):

        for existing_book in self.available_books:

            if (
                existing_book.title == book.title and
                existing_book.author == book.author and
                existing_book.category == book.category
            ):

                existing_book.copies += book.copies

                print(
                    f"{book.copies} copies added to {book.title}"
                )

                return



        self.available_books.append(book)

        print(
            f"{book.title} added to library."
        )




    def remove_book(self, book):

        for existing_book in self.available_books:

            if (
                existing_book.title == book.title and
                existing_book.author == book.author
            ):


                if existing_book.copies > 1:

                    existing_book.copies -= 1

                    print(
                        f"One copy removed. Remaining copies: {existing_book.copies}"
                    )


                else:

                    self.available_books.remove(existing_book)

                    print(
                        f"{book.title} removed completely."
                    )


                return



        print("Book not found.")





    def borrow_book(self, book, member, date):


        for existing_book in self.available_books:


            if (
                existing_book.title == book.title and
                existing_book.author == book.author and
                existing_book.category == book.category
            ):


                if existing_book.copies <= 0:

                    print("Book unavailable.")

                    return



                # check duplicate borrowing

                for borrowed in member.books:

                    if (
                        borrowed.title == existing_book.title and
                        borrowed.author == existing_book.author
                    ):

                        print(
                            f"{member.name} already borrowed this book."
                        )

                        return




                # decrease available copies

                existing_book.copies -= 1



                # add book to member

                member.books.append(existing_book)



                # store borrowed record

                self.borrowed_books.append(
                    {
                        "book": existing_book,
                        "member": member,
                        "date": date
                    }
                )



                # store transaction

                self.transactions.append(
                    {
                        "member": member.name,
                        "book": existing_book.title,
                        "date": date,
                        "action": "Borrowed"
                    }
                )



                print(
                    f"{member.name} borrowed {existing_book.title}"
                )



                # remove if no copies left

                if existing_book.copies == 0:

                    self.available_books.remove(existing_book)



                return




        print("Book not found.")







    def return_book(self, book, member, date):


        borrowed_record = None



        for record in self.borrowed_books:


            if (
                record["member"] == member and
                record["book"].title == book.title
            ):

                borrowed_record = record
                break




        if borrowed_record is None:

            print(
                f"{member.name} did not borrow this book."
            )

            return




        returned_book = borrowed_record["book"]




        # remove from member

        member.books.remove(returned_book)



        # remove borrowed record

        self.borrowed_books.remove(borrowed_record)




        # add copy back

        found = False



        for existing_book in self.available_books:


            if (
                existing_book.title == returned_book.title and
                existing_book.author == returned_book.author and
                existing_book.category == returned_book.category
            ):


                existing_book.copies += 1

                found = True

                break




        if not found:


            returned_book.copies = 1

            self.available_books.append(returned_book)




        self.transactions.append(
            {
                "member": member.name,
                "book": returned_book.title,
                "date": date,
                "action": "Returned"
            }
        )



        print(
            f"{member.name} returned {returned_book.title}"
        )







    def display_available_books(self):

        print("\nAvailable Books")
        print("----------------")


        if not self.available_books:

            print("No books available.")

            return



        for book in self.available_books:

            print(
                f"{book.title} | "
                f"{book.author} | "
                f"{book.category} | "
                f"Copies: {book.copies}"
            )







    def display_borrowed_books(self):

        print("\nBorrowed Books")
        print("----------------")


        if not self.borrowed_books:

            print("No borrowed books.")

            return



        for record in self.borrowed_books:

            print(
                f"{record['book'].title} borrowed by {record['member'].name}"
            )







    def transaction_history(self):

        print("\nTransaction History")
        print("-------------------")


        if not self.transactions:

            print("No transactions.")

            return



        for transaction in self.transactions:

            print(
                f"{transaction['member']} | "
                f"{transaction['book']} | "
                f"{transaction['date']} | "
                f"{transaction['action']}"
            )







    def get_books_by_category(self, category):


        print(
            f"\nBooks in category: {category}"
        )


        found = False



        for book in self.available_books:


            if book.category.lower() == category.lower():

                print(
                    book.display()
                )

                found = True




        if not found:

            print("No books found.")







# ================= TESTING =================



book1 = Book(
    "Python Programming",
    "John Smith",
    "Programming",
    2
)


book2 = Book(
    "Data Science",
    "Alice Brown",
    "Technology",
    1
)


book3 = Book(
    "Mathematics",
    "Ramanujan",
    "Maths",
    1
)



member1 = Member(
    "Ali",
    101
)



library = Library(
    "City Library"
)



library.add_book(book1)
library.add_book(book2)
library.add_book(book3)



library.display_available_books()



library.borrow_book(
    book1,
    member1,
    "08-07-2026"
)



member1.display_member_info()



library.display_available_books()



library.display_borrowed_books()



library.return_book(
    book1,
    member1,
    "10-07-2026"
)



library.display_available_books()



library.display_borrowed_books()



library.transaction_history()



library.get_books_by_category("Maths")