
from abc import ABC, abstractmethod
class Book:
    def __init__(self,title,author,isbn,available):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.available=available
        print(f'{self.title} written by {self.author} is {"available" if available else "not available"}')

class Member(ABC):
    def __init__(self,name,_member_id):
        self.name=name
        self._member_id=_member_id
        print(f"The new Member is {self.name}")
    @abstractmethod
    def borrow_book(self,isbn):
        pass
    
class Student(Member):
    def __init__(self,name,_member_id):
        super().__init__(name,_member_id)
    def borrow_book(self,isbn):
        print(f'Member {self.name} {self._member_id} borrowed {isbn}')

class Teacher(Member):
    def __init__(self,name,_member_id):
        super().__init__(name,_member_id)
    def borrow_book(self,isbn):
        print(f'Member {self.name} ({self._member_id}) borrowed {isbn}')

class Library:
    def __init__(self):
        self.books={}
        self.members={}

b1=Book("Harry Potter and the Goblet of Fire","J.K.Rowling",9780439139595,True)
s1 = Student("Tharusha", "st001")
t1 = Teacher("Mr. Perera", "t001")
s1.borrow_book(9780439139595)