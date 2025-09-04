
from abc import ABC, abstractmethod
class Book:
    def __init__(self,title,author,isbn,available=True):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.available=available
        self.borrowed_by = None
        print(f'{self.title} written by {self.author} is {"available" if available else "not available"}')

class Member(ABC):
    def __init__(self,name,_member_id):
        self.name=name
        self._member_id=_member_id
        self.borrowed_books=[]
        print(f"The new Member is {self.name}")
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
            print(f"{self.name} successfully borrowed {book.title} borrowed by {book.borrowed_by.name}")
        else:
            print(f"{self.name} cannot borrow {book.title} : {msg}")
    
    def return_book(self,book):
        if book.available:
            print(f"{book.title} is already in the system.")
        else:
            borrower=book.borrowed_by
            book.available=True
            book.borrowed_by=None
            borrower.borrowed_books.remove(book)
            print(f"{self.name} returned {borrower.name}'s book: {book.title}")
    def list_borrowed_books(self):
        if not self.borrowed_books:
            print(f'{self.name} has no books borrowed')
        else:
            print(f"Books borrowed by {self.name}")
            for x in self.borrowed_books:
                print(f"- {x.title} by {x.author}")


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
        print('added a new member')
    def add_book(self,book):
        self.books[book.isbn]=book
        print('added a new book')
    def del_member(self,member):
        if member._member_id in self.members:
            self.members.pop(member._member_id)
            print(f"Deleted the member {member.name}")
        else:
            print('Member not found')
    def del_book(self,book):
        if book.isbn in self.books:
            self.books.pop(book.isbn)
            print(f'Deleted the book {book.title}' )
        else:
            print("Book not found")
    def find_member(self,memberid):
        if memberid in self.members:
            membername=self.members[memberid]
            print(f'The ID "{memberid}" belongs to the member "{membername.name}"')
            membername.list_borrowed_books()
        else:
            print("Member not found")
    def find_book(self,isbn):
        if isbn in self.books:
            bookname=self.books[isbn]
            if bookname.available:
                print(f"The book with the isbn {isbn} is available")
            else:
                print(f"The book {bookname.title} is unavailable.",end=" ")
                print(f"It was borrowed by {bookname.borrowed_by.name}")
        else:
            print("That book is not available in this library")

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
s1.borrow_book(b1)
s1.borrow_book(b2)
s1.borrow_book(b3)
s1.borrow_book(b4)
s2.return_book(b1)
s1.borrow_book(b4)
s1.list_borrowed_books()
library.find_member("st001")
library.find_member("t002")
library.find_book(9781501175466)
#print(library.members)
#print(library.books)