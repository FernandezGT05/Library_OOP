import json
import requests
from abc import ABC, abstractmethod

def get_book_info(isbn):
    
    url=f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response=requests.get(url)
    if response.status_code!=200:
        print(response.status_code)
        return False
    book_data=response.json()
    if 'items'not in book_data:
        return None
    volume_data=book_data['items'][0]['volumeInfo']
    return volume_data

class Book:
    def __init__(self,title,author,isbn,book_info=None,available=True,stored_info=None):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.available=available
        self.borrowed_by = None
        if stored_info:
            self.description=stored_info.get('description',"None")
            self.page_count=stored_info.get('page_count','Unknown')
            self.published_date=stored_info.get('published_date','Unknown')
            self.publisher=stored_info.get('publisher','Unknown')
        else:
            if book_info is None:
                book_info=get_book_info(isbn)
            self.description=book_info.get('description',"None")
            self.page_count=book_info.get('pageCount','Unknown')
            self.published_date=book_info.get('publishedDate','Unknown')
            self.publisher=book_info.get('publisher','Unknown')
        print(f'{self.title} written by {self.author} is {"available" if available else "not available"}')

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
            library.save_data()
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
            library.save_data()
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
        self.load_data()
    def save_data(self):
        data={
            "books":[{"Title":b.title,
                      "Author":b.author,
                      "ISBN":b.isbn,
                      "Available":b.available,
                      "Description":b.description,
                      "Borrowed By":b.borrowed_by._member_id if b.borrowed_by else None,
                      "Page Count":b.page_count,
                      "Published Date":b.published_date,
                      "Publisher":b.publisher}
                for b in self.books.values()
            ],
            "members":[{"Name":m.name,"ID":m._member_id,"Type":m.__class__.__name__,
                        "Borrowed books":[{"Title":book.title,"ISBN":book.isbn} for book in m.borrowed_books]}
                for m in self.members.values()

            ]
        }
        with open("data.json","w")as f:
            json.dump(data,f,indent=4)
    
    def load_data(self):
        try:
            with open("data.json","r")as f:
                data=json.load(f)
        except FileNotFoundError:
            print("file not found")
            return
        #loading books
        for b in data.get("books",[]):
            isbn=str(b["ISBN"])
            stored_info={
                "description":b.get('Description','None'),
                "page_count":b.get('Page Count','Unknown'),
                "published_date":b.get('Published Date','Unknown'),
                "publisher":b.get('Publisher','Unknown')
            }
            book=Book(b["Title"],b["Author"],b["ISBN"],available=b.get("Available",True),stored_info=stored_info)
            self.books[isbn]=book
        #loading members
        for m in data.get("members",[]):
            if m["Type"]=='Student':
                member=Student(m["Name"],m["ID"])
            elif m["Type"]=="Teacher":
                member=Teacher(m["Name"],m["ID"])
            else:
                continue
            self.members[m["ID"]]=member
            #connecting them
            for borrowed in m.get("Borrowed books",[]):
                book=self.books.get(borrowed["ISBN"])
                if not book:
                    continue
                member.borrowed_books.append(book)
                book.borrowed_by=member
                book.available=False


    def add_members(self,member):
        self.members[member._member_id]=member
        self.save_data()
    def add_book(self,book):
        self.books[book.isbn]=book
        self.save_data()
    def del_member(self,member_id):
        if member_id in self.members:
            deleted_member=self.members.pop(member_id)
            print(f"Deleted the member {deleted_member.name}")
            self.save_data()
            input("\nPress Enter to proceed...")
            
        else:
            print('Member not found')
            input("\nPress Enter to proceed...")
    def del_book(self,isbn):
        if isbn in self.books:
            deleted_book=self.books.pop(isbn)
            print(f'Deleted the book {deleted_book.title}' )
            self.save_data()
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
    print("9. Delete a book")
    print("10. Delete a member")
    print("11. Exit")
    
    choice = input("Enter your choice: ")
    if choice == "1":
        c=input("Enter the isbn: ")
        book_info=get_book_info(c)
        if not book_info:
            print("Book info could not be retrieved")
            continue
        a=book_info['title']
        b=book_info['authors'][0]
        d=Book(a,b,c,book_info=book_info)
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
            id=input("Input member ID: ").strip()
            if id.lower()=="cancel":
                break
            else:
                member=library.members.get(id)
                if member==None:
                    print("Invalid member ID\n")
                    continue
                book=None
                while True:
                    isbn=input("Enter the isbn: ").strip()
                    if isbn.lower()=="cancel":
                        break
                    else:
                        book=library.books.get(isbn)
                        if book==None:
                            print("Invalid isbn\n")
                            continue
                        break
                if member and book:
                    member.borrow_book(book)
                    break
    elif choice=="4":
        while True:
            id=input("Input the member ID: ").strip()
            if id.lower()=="cancel":
                break
            else:
                member=library.members.get(id)
                if member==None:
                    print("Invalid member ID\n")
                    continue
                book=None
                while True:
                    isbn=input("Enter the isbn: ").strip()
                    if isbn.lower()=="cancel":
                        break
                    else:
                        book=library.books.get(isbn)
                        if book==None:
                            print("Invalid isbn\n")
                            continue
                        elif book:
                            break
                if book:
                    member.return_book(book)
                    break
    elif choice=="5":
        id=input("Enter the member ID: ")
        library.find_member(id)
    
    elif choice=="6":
        isbn=input("Enter the isbn: ")
        if isbn in library.books:
            book_info=get_book_info(isbn)
            if not book_info:
                print("Book info could not be retrieved.")
                continue
            book=library.books.get(isbn)
            print("----Book info----")
            print(f"Title: {book_info['title']}")
            print(f"Author: {book_info['authors'][0]}")
            print(f"ISBN: {isbn}")
            print(f"Description: {book.description}")
            print(f"Availability: {book.available}")
            borrowed_by = book.borrowed_by.name if book.borrowed_by else "None"
            print(f"Borrowed By: {borrowed_by}")
            print(f"Page Count: {book.page_count}")
            print(f"Publisher: {book.publisher}")
            print(f"Published Date: {book.published_date}")
            input("\nPress Enter to proceed...")
        else:
            print("Book not in the Library")
            input("\nPress Enter to proceed...")
    elif choice=="7":
        library.list_all_available_books()
    elif choice=="8":
        library.list_all_borrowed_books()
    elif choice=="9":
        d=input("Enter the isbn: ")
        library.del_book(d)
    elif choice=="10":
        d=input("Enter the member ID: ")
        library.del_member(d)
    elif choice=="11":
        print("Exiting the system.")
        break
    else:
        print("Invalid choice.Try again")
        input("\nPress Enter to proceed...")