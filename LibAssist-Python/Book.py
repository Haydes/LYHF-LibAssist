class Book:

    def __init__(self, ISBN, title, author, pubDate, user):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.pubDate = pubDate
        self.user = user

    def setUser(self, user):
        self.user = user

