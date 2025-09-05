
from abc import ABC, abstractmethod
class Book:
    def __init__(self,title,author,isbn,available=True):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.available=available
        self.borrowed_by = None
        print(f'{self.title} written by {self.author} is {"available" if available else "not available"}')
        input("\nPress Enter to proceed...")

class Member(ABC):
    def __init__(self,name,_member_id):
        self.name=name
        self._member_id=_member_id
        self.borrowed_books=[]
    @abstractmethod
    def get_borrow_limit(self):
        pass
    
    def can_borrow_book(self,book):
        if book.available:
            if len(self.borrowed_books)>=self.get_borrow_limit():
                return False, f"{self.name} has reaches the borrowing limit"
            else: 
                return True,'can borrow'
        return False ,"Book not available"
        
    def borrow_book(self,book):
        can_borrow, msg=self.can_borrow_book(book)
        if can_borrow:
            self.borrowed_books.append(book)
            book.borrowed_by=self
            book.available=False
            print(f"{self.name} successfully borrowed {book.title}")
            input("\nPress Enter to proceed...")
        else:
            print(f"{self.name} cannot borrow {book.title} : {msg}")
            input("\nPress Enter to proceed...")

    
    def return_book(self,book):
        if book.available:
            print(f"{book.title} is already in the system.")
            input("\nPress Enter to proceed...")
        else:
            borrower=book.borrowed_by
            book.available=True
            book.borrowed_by=None
            borrower.borrowed_books.remove(book)
            if self.name==borrower.name:
                print(f"{self.name} returned the book: {book.title}")
                input("\nPress Enter to proceed...")
            else:
                print(f"{self.name} returned {borrower.name}'s book: {book.title}")
                input("\nPress Enter to proceed...")
            
    def list_borrowed_books(self):
        if not self.borrowed_books:
            print(f'{self.name} has no books borrowed')
            input("\nPress Enter to proceed...")
        else:
            print(f"Books borrowed by {self.name}")
            for x in self.borrowed_books:
                print(f"- {x.title} by {x.author}")
            input("\nPress Enter to proceed...")


class Student(Member):
    def get_borrow_limit(self):
        return 3
class Teacher(Member):
    def get_borrow_limit(self):
        return 5
class Library:
    def __init__(self):
        self.books={}
        self.members={}
    def add_members(self,member):
        self.members[member._member_id]=member
    def add_book(self,book):
        self.books[book.isbn]=book
    def del_member(self,member):
        if member._member_id in self.members:
            self.members.pop(member._member_id)
            print(f"Deleted the member {member.name}")
            input("\nPress Enter to proceed...")
        else:
            print('Member not found')
            input("\nPress Enter to proceed...")
    def del_book(self,book):
        if book.isbn in self.books:
            self.books.pop(book.isbn)
            print(f'Deleted the book {book.title}' )
            input("\nPress Enter to proceed...")
        else:
            print("Book not found")
            input("\nPress Enter to proceed...")
    def find_member(self,memberid):
        if memberid in self.members:
            membername=self.members[memberid]
            print(f'The ID "{memberid}" belongs to the member "{membername.name}"')
            membername.list_borrowed_books()
        else:
            print("Member not found")
            input("\nPress Enter to proceed...")
    def find_book(self,isbn):
        if isbn in self.books:
            bookname=self.books[isbn]
            if bookname.available:
                print(f"The book with the isbn '{isbn}' is available")
                input("\nPress Enter to proceed...")
            else:
                print(f"The book {bookname.title} is unavailable.",end=" ")
                print(f"It was borrowed by {bookname.borrowed_by.name}")
                input("\nPress Enter to proceed...")
        else:
            print("That book is not available in this library")
            input("\nPress Enter to proceed...")
    def list_all_available_books(self):
        print("----Available Books----")
        x=False
        for books in self.books.values():
            if books.available:
                print(f"-{books.title} by {books.author} ({books.isbn})")
                x=True
        if x==False:
            print("There are no books available")
        input("\nPress Enter to proceed...")
            
    def list_all_borrowed_books(self):
        print("----Borrowed Books----")
        x=False
        for books in self.books.values():
            if not books.available:
                print(f"-{books.borrowed_by.name} borrowed --> {books.title}")
                x=True
        if x==False:
            print("No books are currently borrowed")
        input("\nPress Enter to proceed...")

library=Library()

b1=Book("Harry Potter and the Goblet of Fire","J.K.Rowling",9780439139595)
library.add_book(b1)
b2=Book("IT : A Novel","Stephen King",9781501175466)
library.add_book(b2)
b3=Book('Game of Thrones: A Song of Ice and Fire','George R.R. Martin',9780553573404)
library.add_book(b3)
b4=Book("Diary of a Wimpy Kid: The Getaway",'Jeff Kinney',9780241344279)
library.add_book(b4)
s1 = Student("Tharusha", "st001")
library.add_members(s1)
t1 = Teacher("Mr. Perera", "t001")
library.add_members(t1)
s2= Student("Fernandez","st002")
library.add_members(s2)
t2=Teacher("Mrs. silva",'t002')
library.add_members(t2)
print('\n')

while True:
    print("\n--- Library Menu ---")
    print("1. Add a book")
    print("2. Add a member")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Find member by ID")
    print("6. Find book by isbn")
    print("7. List all available books")
    print("8. List all borrowed books")
    print("9. Exit")
    
    choice = input("Enter your choice: ")
    if choice == "1":
        a=input("Enter book title: ")
        b=input("Enter the author: ")
        c=int(input("Enter the isbn: "))
        d=Book(a,b,c)
        library.add_book(d)
    elif choice=="2":
        while True:
            d=input("Are you a student/teacher? : ").strip().lower()
            if d=="student":
                a=input("Enter the name: ")
                b=input("Enter the member ID: ")
                c=Student(a,b)
                library.add_members(c)
                print(f"Member {a} added")
                break
            elif d=="teacher":
                a=input("Enter the name: ")
                b=input("Enter the member ID: ")
                c=Teacher(a,b)
                library.add_members(c)
                print(f"Member {a} added")
                break
            else:
                print("Invalid.Try again")
    elif choice=="3":
        while True:
            id=input("Input member ID: ")
            member=library.members.get(id)
            if member==None:
                print("Invalid member ID\n")
                continue
            while True:
                isbn=input("Enter the isbn: ")
                book=library.books.get(int(isbn))
                if book==None:
                    print("Invalid isbn\n")
                elif book:
                    break
            if member and book:
                member.borrow_book(book)
                break
    elif choice=="4":
        while True:
            id=input("Input the member ID: ")
            member=library.members.get(id)
            if member==None:
                print("Invalid member ID\n")
                continue
            while True:
                isbn=input("Enter the isbn: ")
                book=library.books.get(int(isbn))
                if book==None:
                    print("Invalid isbn\n")
                    continue
                elif book:
                    break
            member.return_book(book)
            break
    elif choice=="5":
        id=input("Enter the member ID: ")
        library.find_member(id)
    elif choice=="6":
        isbn=input("Enter the isbn: ")
        library.find_book(int(isbn))
    elif choice=="7":
        library.list_all_available_books()
    elif choice=="8":
        library.list_all_borrowed_books()
    elif choice=="9":
        print("Exiting the system.")
        break
    else:
        print("Invalid choice.Try again")
        input("\nPress Enter to proceed...")