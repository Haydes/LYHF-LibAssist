#!/usr/bin/env python3

from requests import Session
from time import perf_counter

SITE_URL = 'http://localhost:5000'

def test_many_logins():
    nlogins = 100
    sessions = []
    for i in range(0, nlogins):
        s = Session()
        user = "test-login-user%d" % i
        pswd = "test-login-pass%d" % i
        cred = {'username': user, 'password': pswd}

        # Create new user.
        # If we already created that user, it doesn't matter.
        s.post("%s/register" % SITE_URL, data=cred)

        # Login that user.
        # If we fail this assertion, go do regenerate_database and try again.
        login = s.post("%s/login" % SITE_URL, data=cred)
        assert bytes('Invalid credentials', 'utf-8') not in login.content
        sessions.append(s)

        # Attempt a search.
        t1 = perf_counter()
        s.get("%s/showbooks" % SITE_URL)
        t2 = perf_counter()

        # Performance for searches should be less than 10 seconds.
        # This should hold true even when 100 sessions are active.
        assert (t2 - t1) < 10
    assert nlogins == len(sessions)

