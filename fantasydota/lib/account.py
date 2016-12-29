
def check_invalid_password(password, confirm_password):
    if len(password) < 6:
        return {"message": "Password too short. 6 characters minimum please"}
    elif len(password) > 20:
        return {"message": "Password too long. 20 characters maximum please"}
    elif confirm_password != password:
        return{"message": "Passwords did not match"}
    else:
        return False
