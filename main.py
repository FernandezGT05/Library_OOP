
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
            print(f"{self.name} successfully borrowed {book.title}")
        else:
            print(f"{self.name} cannot borrow {book.title} : {msg}")
    
class Student(Member):
    def __init__(self,name,_member_id):
        super().__init__(name,_member_id)
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


library=Library()

b1=Book("Harry Potter and the Goblet of Fire","J.K.Rowling",9780439139595)
b2=Book("IT : A Novel","Stephen King",9781501175466)
b3=Book('Game of Thrones: A Song of Ice and Fire','George R.R. Martin',9780553573404)
b4=Book("Diary of a Wimpy Kid: The Getaway",'Jeff Kinney',9780241344279)
s1 = Student("Tharusha", "st001")
t1 = Teacher("Mr. Perera", "t001")
s2= Student("Fernandez","st002")
t2=Teacher("Mrs. silva",'t002')
library.add_members(s1)
library.add_members(t1)
library.add_members(s2)
library.add_members(t2)
library.add_book(b1)
library.add_book(b2)
library.add_book(b3)
library.add_book(b4)
s1.borrow_book(b1)
s1.borrow_book(b2)
s1.borrow_book(b3)
s1.borrow_book(b4)
#print(library.members)
#print(library.books)