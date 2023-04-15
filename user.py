
class User:

    def __init__(self, name, personal_id, email, permission):
        self._name = name
        self._personal_id = personal_id
        self._email = email
        self._permission = permission

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



