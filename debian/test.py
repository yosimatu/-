#!/usr/bin/python3
#
# my_view.py … ビュー
from http import cookies

import my_model

# ●ログイン画面の HTML を表示する処理
def login(level, msg):
    # 引数: level … 前の処理で発生したメッセージの表示レベル
    # msg … 前の処理で指示されたメッセージ
    # 戻り値: なし
    #
    prv_print_html_header()

    print('<body><br><br>')
    print('<font size="+2">Debian Code Name Access Tool</font><br>')
    print('<br>')

    print('<font size="+0">ログイン画面</font><br>')
    print('<br>')
    # 「ユーザ ID」と「パスワード」のテキストボックス、「ログイン」ボタンの表示
    print('<form method="POST" action="./index.py">')
    print(' <label> ＩＤ：</label>')
    print(' <input type="text" size="30" name="UID">')
    print(' <br>')
    print(' <label>パスワード：</label>')
    print(' <input type="password" size="30" name="PASS">')
    print(' <br><br>')
    print(' <button type="submit" name="NEXT_MODE" value="SELECT">ログイン</button>')
    print('</form>')
    print('<br><br>')
    if msg is not None:
        # メッセージが指示された場合のみ出力する
        color = prv_get_color(level)
        print(' <font color="' + color + '">' + msg + '</font><br>')
    print(' </body>')
    print('</html>')
    return

# ●データの一覧を出力する HTML を表示する処理
def selectall(uid, pas, level, msg):
    # 引数: uid … ユーザ ID
    # pas … パスワード
    # level … 前の処理で発生したメッセージの表示レベル
    # msg … 前の処理で発生したメッセージ
    # 戻り値: なし
    #
    prv_print_html_cookie_header(uid, pas)

    print('<body><br><br>')
    print('<font size="+2">Debian Code Name Access Tool</font><br>')
    print('<br>')

    # メッセージ出力
    color = prv_get_color(level)
    print('<font color="' + color + '">' + msg + '</font><br>')

    # データベース(debiadb)の接続をリクエスト
    db = my_model.dbconnect(uid, pas)
    if db is not None:
        # 正常に接続した場合
        # SELECT クエリソースの定義
        sqlquery = "SELECT * FROM deb_list ORDER BY "
        sqlquery = sqlquery + "********;"
        # クエリ実行（カーソルオブジェクトを取得）のリクエスト
        cur = my_model.select(db, sqlquery)

        if cur is not None:
            # カーソルを取得できた時の処理
            # 「ログアウト」ボタンの表示
            print('<form method="POST" name="form1" action="./index.py">')
            print(' <button type="submit" name="NEXT_MODE" value="LOGOUT">ログアウト</button>')
            print('</form>')

            if cur.rowcount > 0:
                # 取得したレコードが 1 件以上あった場合の処理
                print('<table border=1>')
                i = 0
                # 見出しの出力
                print('<tr><th>No.</th>', end='')
                print('<th>バージョン番号</th><th>コードネーム</th>',end='')
                print('</tr>')

                for row in cur:
                    # カーソルから 1 件ずつ行(row)を取得する
                    i = i + 1
                    print('<tr>', end='')
                    # 「No.」列のデータの表示
                    print('<td align="right">' + str(i) + '</td>', end='')
                    # 「バージョン番号」列のデータの表示
                    print('<td align="center">' + row[0] + '</td>', end='')
                    # 「コードネーム」列のデータの表示
                    print('<td align="left">' + row[1] + '</td>')
                    print('</tr>')

                print('</table>')
                # カーソルを閉じる
                my_model.close(cur)
            else:
                print('データがありませんでした。<br>')
                # カーソルを閉じる
                my_model.close(cur)
        else:
            print('データの抽出ができません（アクセス権エラー）。<br>')
        # データベースを閉じる
        my_model.dbclose(db)
    else:
        print('データベースに接続できませんでした。<br>')

    print('</body>')
    print('</html>')
    return

# ●エラーメッセージを HTML 表示する処理
def error(uid, pas, mode, msg):
    # 引数: uid … ユーザ ID
    # pas … パスワード
    # mode … NEXT_MODE 情報
    # msg … 出力するメッセージ
    # 戻り値: なし
    #
    prv_print_html_cookie_header(uid, pas)

    print('<body><br><br>')
    print('<font size="+2">Debian Code Name Access Tool</font><br>')
    print('<br>')
    print('<font size="+0" color="Red">' + msg + '</font><br><br>')
    print('<font size="+0" color="Blue"> MODE : ' + mode + '</font><br><br>')
    print('<font size="+0">再度ログインしてください。</font><br>')
    # 「ＯＫ」ボタンの表示
    print('<form method="POST" action="./index.py">')
    print(' <button type="submit" name="NEXT_MODE" value="LOGIN">ＯＫ</button>')
    print('</form>')
    print('</body>')
    print('</html>')
    return

# ●レベルからメッセージのカラー名を取得する処理
def prv_get_color(level):
    # 引数 メッセージのレベル
    # 戻り値: 'Black' … 'NORM'(Normal or default)
    # 'Blue' … 'INFO'(Information)
    # 'Orange' … 'CAUTION'(Caution)
    # 'Red' … 'WARN'(Warnning)
    #
    if level == 'INFO':
        return '********'
    elif level == 'CAUTION':
        return '********'
    elif level == 'WARN':
        return '********'
    else: # level == 'NORM'
        return '********'
# ●HTML にヘッダー情報出力する処理
def prv_print_html_header():
    # 引数: なし
    # 戻り値: なし
    #
    uid = None
    pas = None
    ********(uid, pas)
    return

# ●HTML にクッキー情報とヘッダー情報を出力する処理
def prv_print_html_cookie_header(uid, pas):
    # 引数: uid … ユーザ ID
    # pas … パスワード
    # 戻り値: なし
    #
    print('Content-Type: text/html; charset=UTF-8;')

    if uid is not None and pas is not None:
        # uid が指定されている場合はクッキー情報を出力する
        cookie = cookies.SimpleCookie()
        cookie['UID'] = uid
        cookie['UID']['secure'] = True
        cookie['PASS'] = pas
        cookie['PASS']['secure'] = True
        print(cookie.output())
    else:
        uid が None の場合クッキー情報は出力しない

    print()

    print('<!DOCTYPE html>')
    print('<html lang="ja">')
    print('<head>')
    print('<meta http-equiv="CONTENT-TYPE" content="text/html; charset=utf-8" />')
    print('<title>Debian Code Name List</title>')
    print('</head>')
    return
