import hashlib
import json


def handle_by_md5(user_id, user_pw):
    """
    Encrypt user's data.

    :param user_id:
    :param user_pw:
    :return: dict
    """
    md5_id = hashlib.md5()
    md5_password = hashlib.md5()
    md5_id.update(user_id.encode(encoding="utf-8"))
    md5_password.update(user_pw.encode(encoding="utf-8"))

    md5_dict = {md5_id.hexdigest(): md5_password.hexdigest()}
    return md5_dict


def handle_by_json(md5_dict):
    """
    Write user's encrypted data to to json file.

    :param data:
    :return: None
    """
    with open("users.json", "r", encoding="utf-8") as file:
        model = json.load(file)

    for key in md5_dict:
        model[key] = md5_dict[key]

    obj = json.dumps(model)
    with open("users.json", "w") as file:
        file.write(obj)


if __name__ == '__main__':
    account_num = input("Input your account number: ")
    password = input("Input your password: ")

    md5_dict = handle_by_md5(account_num, password)
    handle_by_json(md5_dict)


