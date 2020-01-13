import requests
from hashlib import md5

def _hash_pass(data):
    return md5(data.encode("utf-8")).hexdigest()

class Zipd:
    def __init__(self, address, username, password):
        self.address = address if address[:len(address)] == "/" else address + "/"
        self.username = username
        self.password = md5(password.encode("utf-8")).hexdigest()
        self.token = ""

    def get_token(self):
        body = {"username": self.username, "password": self.password}
        url = self.address + "api/getLogin"
        
        response = requests.post(url, data=body).json()
        if response["status"] == "success":
            self.token = response["token"]
            return self.token
        elif response["status"] == "error":
            raise Exception(response["error"])

    def generic_request(self, body, extension):
        url = self.address + extension
        response = requests.get(url, params=body).json()
        return response

    def generic_post(self, body, extension):
        url = self.address + extension
        response = requests.post(url, data=body).json()
        return response

    def log_out(self):
        return self.generic_request({"token": self.token}, "api/deleteLogin")

    def get_user_files(self):
        return self.generic_request({"token": self.token}, "api/getUserFiles")

    def change_pass(self, new):
        result = self.generic_post({"token": self.token, "old": self.password, "new": md5(new)}, "api/changePass")
        if result["status"] == "error":
            return result
        else:
            self.password = md5(new)
            return result

    def delete_file(self, id):
        return self.generic_request({"token": self.token, "id": id}, "api/deleteFile")

    def get_file(self, id):
        body = {"token": self.token, "id": id}
        url = self.address + "api/getFile"
        response = requests.get(url, params=body)
        return response

    def get_image_thumbnail(self, id):
        body = {"token": self.token, "id": id}
        url = self.address + "api/getImageThumbnail"
        response = requests.get(url, params=body)
        return response

    def get_user_role(self, user):
        return self.generic_request({"token": self.token, "user": user}, "api/getUserRole")

    def upload_files(self, files, tag):
        body = {"token": self.token, "tag": tag}
        url = self.address + "api/uploadFile"
        response = requests.post(url, data=body, files=files)
        try:
            return response.json()
        except:
            return response

    def upload_single_file(self, file, tag):
        body = {"token": self.token, "tag": tag}
        url = self.address + "api/uploadSingleFile"
        response = requests.post(url, data=body, files=files)
        try:
            return response.json()
        except:
            return response

    def admin_add_user(self, user, pw):
        return self.generic_post({"token": self.token, "name": user, "pass": pw}, "api/admin/addUser")

    def admin_delete_user(self, user):
        return self.generic_request({"token": self.token, "name": user}, "api/admin/deleteUser")

    def admin_filefix(self):
        return self.generic_request({"token": self.token}, "api/admin/filefix")

    def admin_get_gets(self):
        return self.generic_request({"token": self.token}, "api/admin/getGets")

    def admin_get_tokens(self):
        return self.generic_request({"token": self.token}, "api/admin/getTokens")

    def admin_get_user_list(self):
        return self.generic_request({"token": self.token}, "api/admin/getUserList")

    def admin_set_user_password(self, user, new):
        return self.generic_post({"token": self.token, "name": user, "password": _hash_pass(new)}, "api/admin/setUserPassword")

    def admin_wipe_user(self, user):
        return self.generic_get({"token": self.token, "name": user}, "api/admin/wipeUser")