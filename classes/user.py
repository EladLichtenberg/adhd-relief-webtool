import json


class User:

    def __init__(self, name, personal_id, permission, email, phone=None):
        self.name = name
        self.personal_id = personal_id
        self.email = email
        self.permission = permission
        self.phone = phone



    def to_dict(self):
        temp_dict = {
            "personal_id": self.personal_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
        return temp_dict

    def json(self):
        temp_dict = self.to_dict()
        return json.dumps(temp_dict, indent=4)

    def login(self):
        pass

