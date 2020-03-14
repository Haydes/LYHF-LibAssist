class Book:

    def __init__(self, ISBN, title, author, pubDate, username):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.pubDate = pubDate
        self.user = username

    def setUser(self, user):
        self.user = user
