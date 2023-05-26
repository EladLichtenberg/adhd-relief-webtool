import json


class User:

    def __init__(self, name, personal_id, email, permission, phone=None):
        self._name = name
        self._personal_id = personal_id
        self._email = email
        self._permission = permission
        self._phone = phone

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def personal_id(self):
        return self._personal_id

    @personal_id.setter
    def personal_id(self, personal_id):
        self._personal_id = personal_id

    @property
    def permission(self):
        return self._permission

    @permission.setter
    def permission(self, name):
        self._permission = name

    def to_dict(self):
        temp_dict = {
            "personal_id": self._personal_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone
        }
        return temp_dict

    def json(self):
        temp_dict = self.to_dict()
        return json.dumps(temp_dict, indent=4)

    def login(self):
        pass


class Teacher(User):

    def create_program(self):
        pass

    def insert_physical_attributes(self):
        pass

    def view_program(self):
        pass

    def compare_programs(self):
        pass

    def notify_parent(self):
        pass


class Parent(User):

    def view_program(self):
        pass

    def get_notification(self):
        pass

    def view_improvement(self):
        pass



