import mysql.connector
from mysql.connector import errorcode



def login(username, password):
    loginok = False

    try:
        dbConn = mysql.connector.connect(user='Team5', password='Team5!', host='86.92.147.175', database='VIRT')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    print("DB Connection started")
    cursor = dbConn.cursor()
    query = 'SELECT user_email, user_pwd FROM users WHERE user_email = %s AND user_pwd = %s;'
    cursor.execute(query, (username, password))
    print('User {} has logged in with password {}'.format(username, password))
    result = cursor.fetchall()
    print(result)
    if username == str(result[0][0]) and password == str(result[0][1]):
        loginok = True
    else:
        loginok = False

    return loginok

print(login('ramyad__@hotmail.com', 'qwerty123'))
