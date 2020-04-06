#!/usr/bin/env python3

from requests import Session
from time import sleep


SITE_URL = 'http://localhost:5000'


# Test that the server is available for a 24 hour period.
def test_reliability():
    def check_server():
        s = Session()
        cred = {'username': 'Jack', 'password': 'ilovefruits'}

        # Attempt a login. This should not fail.
        login = s.post("%s/login" % SITE_URL, data=cred)
        assert bytes('Invalid credentials', 'utf-8') not in login.content
        assert login.status_code == 200

        # Attempt a search. This should also not fail.
        search = s.get("%s/showbooks" % SITE_URL)
        assert search.status_code == 200

        # Logout.
        logout = s.post("%s/logout" % SITE_URL)
        assert logout.status_code == 200

    check_server()
    print("Reliability test 0 successful")
    for i in range(1, 25):
        sleep(3600)
        check_server()
        print("Reliability test %d successful" % i)
