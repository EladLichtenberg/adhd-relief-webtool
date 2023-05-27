INATTENTION = {
    'TASKFOCUS',
    'CARELESS',
    'UNORGAN',
    'EASILYDISTRACT',
    'NOTFINISH',
    'FORGETFUL',
    'DISLIKEEFFORT',
    'LOSINGTHINGS',
    'NOTLISTEN',
}
HYPERACTIVITY = {
    'FIDGET',
    'UNSEATED',
    'RUNNINGCLIMBING',
    'UNQUIET',
    'DRIVENMOTOR'
    'EXCESSIVETALK',
    'BLURTING',
    'IMPATIENT',
    'INTRUDES'
}

map = {
    'TASKFOCUS': ['Aerobics', 'Dance/Yoga'],
    'CARELESS': ['Martial arts', 'Aerobics', 'Dance/Yoga'],
    'UNORGAN': ['Team Games', 'Martial arts'],
    'EASILYDISTRACT': ['Aerobics', 'Dance/.Yoga'],
    'NOTFINISH': ['Team Games', 'Martial arts'],
    'FORGETFUL': ['Martial arts', 'Dance/Yoga'],
    'DISLIKEEFFORT': ['Dance/Yoga'],
    'LOSINGTHINGS': ['Team Games', 'Martial arts', 'Dance/Yoga'],
    'NOTLISTEN': ['Aerobics', 'Dance/Yoga'],
    'FIDGET': ['Dance/Yoga', 'Martial arts'],
    'UNSEATED': ['Martial arts', 'Aerobics', 'Dance/Yoga', 'Team Games'],
    'RUNNINGCLIMBING': ['Martial arts', 'Aerobics', 'Dance/Yoga', 'Team Games'],
    'UNQUIET': ['Team Games', 'Martial arts'],
    'DRIVENMOTOR': ['Team Games'],
    'EXCESSIVETALK': ['Martial arts'],
    'BLURTING': ['Dance/Yoga', 'Team Games'],
    'IMPATIENT': ['Dance/Yoga', 'Team Games'],
    'INTRUDES': ['Dance/Yoga', 'Team Games', 'Martial arts']
}


def get_program(symptoms):
    diagnosis = get_diagnosis(symptoms)
    if diagnosis == "Inattention":
        supplement = 'Iron'
        dosage = "3 times"  # TODO edit
    if diagnosis == "Hyperactivity" or diagnosis == 'Combination':
        supplement = 'Zinc'
        dosage = "2 times"  # TODO edit
    sports = set()
    for symptom in symptoms:
        temp = map[symptom]
        for i in temp:
            sports.add(i)

    return {'diagnosis': diagnosis, 'supplement': {'name': supplement, 'dosage': dosage}, 'sports': sports}  # noqa


def get_diagnosis(symptoms):
    inattention_count = len(INATTENTION.intersection(symptoms))
    hyperactivity_count = len(HYPERACTIVITY.intersection(symptoms))

    if inattention_count >= 6 > hyperactivity_count:
        return "Inattention"
    elif inattention_count < 6 <= hyperactivity_count:
        return "Hyperactivity"
    else:
        return "Combination"


def get_programm_as_string(id, name, data):
    result_string = "ADHD treatment program for:\n\nName: {name}\nID: {id}\n\nRecommendations:\n\nNutritional Supplements:\n- {Supplement}: {Dosage}\n\t- {Description}\n\n"

    result_string = result_string.replace('{name}', name)
    result_string = result_string.replace('{id}', id)
    result_string = result_string.replace('{Supplement}', data['supplement']['name'])
    result_string = result_string.replace('{Dosage}', data['supplement']['dosage'])

    result_string += 'Sports Activities:\n - '
    for sport in data['sports']:
        result_string += sport
        result_string += '\n\t- {Description}\n\n'

    return result_string


if __name__ == '__main__':
    result = get_program(['TASKFOCUS', 'CARELESS'])
    id = '333879096'
    name = 'Nikita'
    strin = get_programm_as_string(id, name, result)
    print(strin)
