from requests import Session
#below are unit tests
###################################
SITE_URL = 'http://localhost:5000'
def test_register():
    #create user
    s = Session()
    user = "Haydes"
    pswd = "111"
    cred = {'username': user, 'password': pswd}
    register = s.post("%s/register" % SITE_URL, data=cred)
    assert bytes('User already exists!', 'utf-8') in register.content

    user = "hhhhhhhhhhhhhhh"
    pswd = "ajbljl"
    cred = {'username': user, 'password': pswd}
    register = s.post("%s/register" % SITE_URL, data=cred)
    assert bytes('Success! User created', 'utf-8') in register.content

def test_login():
    s = Session()
    user = "Haydes"
    pswd = "1112"
    cred = {'username': user, 'password': pswd}
    login = s.post("%s/login" % SITE_URL, data=cred)
    assert bytes('Invalid credentials', 'utf-8') in login.content

def test_checkout():
    s = Session()
    user = "Haydes"
    pswd = "111"
    cred = {'username': user, 'password': pswd}
    s.post("%s/login" % SITE_URL, data=cred)

    data1 = {'bookid': 1234560000, 'idtype': 'use-isbn'}
    checkout = s.post("%s/checkout" % SITE_URL, data=data1)
    assert bytes('You have a checked out book!', 'utf-8') in checkout.content


def test_checkin():
    s = Session()
    user = "Haydes"
    pswd = "111"
    cred = {'username': user, 'password': pswd}
    s.post("%s/login" % SITE_URL, data=cred)

    checkin = s.post("%s/checkin" % SITE_URL)
    assert bytes("You haven't check out any book currently!", 'utf-8') in checkin.content

def test_logout():
    s = Session()
    user = "Haydes"
    pswd = "111"
    cred = {'username': user, 'password': pswd}
    s.post("%s/login" % SITE_URL, data=cred)

    logout = s.post("%s/logout" % SITE_URL)
    assert bytes('Library Assistant Login', 'utf-8') in logout.content

def test_showbooks():
    s = Session()
    user = "Haydes"
    pswd = "111"
    cred = {'username': user, 'password': pswd}
    s.post("%s/login" % SITE_URL, data=cred)

    showbooks = s.get("%s/showbooks" % SITE_URL)
    assert bytes('List of Available Books:', 'utf-8') in showbooks.content

def test_addbook():
    s = Session()
    user = "Haydes"
    pswd = "111"
    cred = {'username': user, 'password': pswd}
    s.post("%s/login" % SITE_URL, data=cred)

    data1 = {'title': 'good guy', 'isbn': 1223456784, 'author': 'Lian', 'pubdate': '2000-12-23'}
    addbook = s.post("%s/addbook" % SITE_URL, data=data1)
    assert bytes('Success! Book entered into database', 'utf-8') in addbook.content