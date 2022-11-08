#!/usr/bin/python3

#index.py

import cgi, os
from http import cookies

import my_ctl

try:
    cookie = cookies.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
except:
    cookie = None

try:
    form = cgi.FieldStorage()
    mode = form.getvalue('NEXT_MODE')
except:
    form = None
    mode = 'LOGIN'

if mode is None:
    mode = 'LOGIN'

if mode is 'LOGIN':
    my_ctl.login()
elif form is not None:
    my_ctl.access(form, cookie)
elif mode == 'LOGOUT':
    my_ctl.logout()
else:
    my_ctl.relogin()
