#!/usr/bin/python3
#
# my_model.py … モデル
#
import mysql.connector
import requests
from requests.auth import HTTPDigestAuth

# ●ユーザ認証処理（ダイジェスト認証版
def auth(uid, pas):
    # 引数: uid … ユーザ ID
    # pas … パスワード
    # 戻り値: 'AUTH_OK … 認証成功
    # 'AUTH_NG' … 認証失敗
    #
    auth_url = 'http://www.y037.home/himitsu/'
    # ダイジェスト認証
    # response :
    # 200 : Authorized Access
    # 401 : Unauthorized Access
    response = requests.get(auth_url, auth=HTTPDigestAuth(uid, pas))

    if response.status_code == 200:
        return 'AUTH_OK'
    else:
        return 'AUTH_NG'

# ●データベース(debiandb)接続処理
def dbconnect(uid, pas):
    # 引数: uid … ユーザ ID
    # pas … パスワード
    # 戻り値: db … データベースの接続（コネクション）オブジェクト（接続成功
    # None … 接続失敗
    #
    # コネクション情報の定義
    hostname = '192.168.21.1'
    dbname = 'debiandb'
    '''
    db = mysql.connector.connect(
            host=hostname,
            user=uid)
    '''
    try:
        #データベースの接続（コネクションオブジェクトの生成）
        db = mysql.connector.connect(
        host=hostname, 
        user=uid, 
        password=pas, 
        database=dbname
        ) 
        return db
    except:
        return None

# ●SELECT(参照)のクエリ実行処理
def select(db, sqlquery):
    # 引数: db … データベースコネクションオブジェクト
    # sqlquery … クエリのソース(string)
    # 戻り値: cur … カーソルオブジェクト（正常実行）
    # None … 異常終了
    #
    try:
        # カーソルオブジェクトの生成
        cur = db.cursor(buffered=True)
        # クエリの実行
        cur.execute(sqlquery)
        return cur
    except:
        return None
# ●カーソルのクローズ処理
def close(cur):
    # 引数: cur … カーソルオブジェクト
    # 戻り値: なし?
    if cur is not None:
        # カーソルを閉じる
        cur.close()
    return

# ●データベースのクローズ処理
def dbclose(db):
    # 引数: db … データベースコネクションオブジェクト
    # 戻り値: なし
    #
    if db is not None:
        # データベースを閉じる
        db.close()
    return
