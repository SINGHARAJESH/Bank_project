
        exit()

def login_user():
    email = input('enter the email: ')
    password = input('enter the password: ')
    sql = "SELECT * FROM accounts WHERE email = %s AND password = %s"
    data = (email, password)
    result = db.execute_query(sql, data)