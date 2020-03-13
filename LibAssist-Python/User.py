class User:

    def __init__(self, username):
        self.username = username
        self.isAdmin = 0
        self.bookISBN = 0

    def borrowBook(self, bookISBN):
        if(self.bookISBN == 0):
            return False
        else:
            self.bookISBN = bookISBN
            return True

    def returnBook(self):
        self.bookISBN = 0

