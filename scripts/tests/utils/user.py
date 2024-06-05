from app.models import User


def save_user_to_db(data):
    """ Save user to db """
    password = data.get("password", None)
    email = data.get("email", None)
    user = User(**data)
    user.set_password(password)
    user.set_email_lower(email)

    exist = user.exists(email)

    if exist:
        return {"error": "Email already exists"}, 400
    else:
        user.save_to_db()

    return user
