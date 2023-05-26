from db import DB


class Pupil:

    def __init__(self, name, personal_id, parent_id, teacher_id, age, sex, symptoms: list):
        self._name = name
        self._personal_id = personal_id
        self._parent_id = parent_id
        self._teacher_id = teacher_id
        self._age = age
        self._sex = sex
        self._symptoms = symptoms

    def get_treatment(self, db: DB):
        symptom = self._symptoms
        query = f"SELCT * FROM sport_relief WHERE symptom={symptom}"
        sports = db.execute_query(query)
        query = f"SELCT * FROM nutrtion_relief WHERE symptom={symptom}"
        nutritions = db.execute_query(query)

        for nutrition in nutritions:
            temp = nutrition['efficiency']*100



