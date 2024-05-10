from auth.py_jwt import signJWT
from db_connection import py_connection
import datetime as datetime
from Crypto.Cipher import DES3
import base64


key = b'Binary--Solution'


# def logdetails(request, decoded, login_time):
#     try:
#         comp_fk = decoded.get("comp_fk")
#         emp_fk = decoded.get("emp_fk")
#         name = decoded.get("username")
#
#         qry = ("INSERT INTO Web_logdetails(comp_fk, comp_name, emp_fk, name, log_in_time) "
#                "VALUES (?, ?, ?, ?, ?)")
#         values = (comp_fk, emp_fk, name, login_time)
#         py_connection.put_result(qry, values)
#         print(qry, values)
#         return {"comp_fk": comp_fk, "emp_fk": emp_fk, "name": name, "login_time": login_time}
#     except Exception as e:
#         print(str(e))
#         return {"message": "Something went wrong!", "rval": 0}



def fn_login(request):
    try:
        username = request.get("username")
        # encrypted_password = "/xoBo7eL2us="
        password = request.get("password")
        encrypted_password = encrypt_password(password, key)
        qry = "SELECT * FROM web_v_logins WHERE Name='{}' AND password='{}'".format(username, encrypted_password)
        result, k = py_connection.get_result_col(qry)
        lst = []
        if result and len(result) > 0:
            for row in result:
                view_data = dict(zip(k, row))
                lst.append(view_data)

            token = signJWT(result[0][2], result[0][1], result[0][11])

            # logdetails(request, decoded, login_time)

            return {"message": "Login successfully", "rval": 1, "data": lst, "token": token}
        else:
            return {"message": "Username or password is incorrect", "rval": 0, "data": [],  "token": ""}
    except Exception as e:
        print(str(e))
        return {"message": "Something went wrong", "rval": 0}


def pad(data):
    padding_length = 8 - len(data) % 8
    return data + bytes([padding_length] * padding_length)


def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]


def encrypt_password(password, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_password = pad(password.encode())
    encrypted_password = cipher.encrypt(padded_password)
    return base64.b64encode(encrypted_password).decode()


def decrypt_password(encrypted_password, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    encrypted_password = base64.b64decode(encrypted_password)
    decrypted_password = cipher.decrypt(encrypted_password)
    return unpad(decrypted_password).decode()


