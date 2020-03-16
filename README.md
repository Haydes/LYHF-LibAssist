# LYHF-LibAssist
Topic: Librarian Assistant  
This is for software quality course project    
We will develop a librarian assistant to help librarians manage common library management tasks, including user registration, book searching, shelving books, checking out books, and returning books. Users can also browse the books in the library and see detailed information about each book selected.

Team info：

Weile Lian weile.lian@wsu.edu 11650752

Xudong Yuan xudong.yuan@wsu.edu 11665818

James Halvorsen james.halvorsen@wsu.edu 11583795

Jiawen Fu jiawen.fu@wsu.edu 11599619

<!--
Java version: JDK1.8  
MySql version: 8.0.19
-->

The documentation PDF should indicate how to use the website. Note that in order to start the server, two scripts must be run:

1. LibAssist-Python/regenerate-database.py
2. LibAssist-Python/main.py

The first of these creates an initial database and populates it with books and users (including the librarian user Haydes). The second starts the server application itself. These applications will depend upon two Python packages: Flask and bcrypt

