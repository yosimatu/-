#!/usr/bin/python3
# my_ctl.py

import my_model, my_view

def login():
    level = 'INFO'
    msg = 'ログインしてください'
    my_view.login(level, msg)
    return

def relogin():
    level = 'WARN'
    msg = '申し訳ありませんが、再度ログインしなおしてください。'
    my_view.login(level, msg)
    return

def logout():
    level = 'INFO'
    msg = 'ログアウトしました'
    my_view.login(level, msg)
    return

def access(form, cookie):
    if form is not None:
        mode = form.getfirst('NEXT_MODE', default='LOGIN')
        uid = form.getfirst('UID')
        pas = form.getfirst('PASS')
        if mode is not None and mode == '':
            mode = 'LOGIN'
    else:
        uid = None
        mode = 'LOGIN'

    if uid is None:
        if cookie is not None:
            try:
                uid = cookie['UID'].value
                pas = cookie['PASS'].value
                if mode == 'LOGIN':
                    mode = 'SELECT'
            except:
                uid = None
        else:
            uid = None
            mode = 'LOGIN'
            relogin()
            return
    if uid is not None:
        stat = my_model.auth(uid, pas)
        if stat == 'AUTH_OK':
            if mode == 'SELECT':
                level = 'NORMAL'
                msg = ''
                my_view.selectall(uid, pas, level, msg)
            elif mode == 'CANCEL':
                level = 'CAUTION'
                msg = '操作をキャンセルしました'
                my_view.selectall(uid, pas, level, msg)
            elif mode == 'LOGOUT':
                logout()
            else:
                msg = 'モードエラーが起きました'
                my_view.error(uid, pas, mode, msg)
        else:
            level = 'WARN'
            msg = 'IDまたはパスワードが一致しません。もう一度やり直してください'
            my_view.login(level, msg)
    else:
        level = 'WARN'
        msg = 'IDが指定されていません。もう一度やり直してください'
        my_view.login(level, msg)

    return
                 

