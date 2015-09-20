from config import db

def try_login(username, password):
    try:
        user = db.select('user', where='username=$username', vars=locals())[0]
        if user.password == password:
            return user
        else:
            return False
    except IndexError:
        return False

def get_user(user_id):
    try:
        return db.select('user', where='id=$user_id', vars=locals())[0]
    except IndexError:
        return None

def get_user_with_email(email):
    try:
        return db.select('user', where='email=$email', vars=locals())[0]
    except IndexError:
        return None

def get_users():
    return db.select('user')


def get_filter(filter_id):
    try:
        return db.select('user_filter', where='id=$filter_id', vars=locals())[0]
    except IndexError:
        return None

def save_filter(user_id, filter):
    db.insert('user_filter', user_id=user_id, filter=filter)

