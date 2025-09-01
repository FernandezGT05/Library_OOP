class Books:
    def __init__(self,title,author,isbn,available):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.available=available
        print(f'{self.title} written by {self.author} is {self.available}')

from abc import ABC, abstractmethod
class Member(ABC):
    def __init__(self):
        pass

class Student(Member):
    def __init__(self):
        pass

class Teacher(Member):
    def __init__(self):
        pass

class Library:
    def __init__(self):
        pass

x=Books("Harry Potter and the Golet of Fire","J.K.Rowling",9780439139595,"available")
