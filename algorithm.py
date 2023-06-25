from db import db

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
    'DRIVENMOTOR',
    'EXCESSIVETALK',
    'BLURTING',
    'IMPATIENT',
    'INTRUDES',
}

map = {
    'TASKFOCUS': ['Aerobics', 'Dance/Yoga'],
    'CARELESS': ['Martial arts', 'Aerobics', 'Dance/Yoga'],
    'UNORGAN': ['Team Games', 'Martial arts'],
    'EASILYDISTRACT': ['Aerobics', 'Dance/Yoga'],
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
    """
        Generates a program based on the provided symptoms.

        The function first obtains a diagnosis by calling the 'get_diagnosis' function with the symptoms.
        Depending on the diagnosis, appropriate supplements are retrieved using the 'find_appropriate_suppliments' function.
        The retrieved supplements are processed to calculate relief and stored in a list.

        The function also determines sports activities based on the symptoms using a mapping called 'map'.

        Finally, the function returns a dictionary containing the diagnosis, supplements, and sports activities.

        Args:
            symptoms (list): A list of symptoms.

        Returns:
            A dictionary with the diagnosis, supplements, and sports activities.
        """
    diagnosis = get_diagnosis(symptoms)
    supplements = []
    res = None
    if diagnosis == "inattention":
        res = find_appropriate_suppliments(['inattention'])
    elif diagnosis == "hyperactivity/impulsivity":
        res = find_appropriate_suppliments(['hyperactivity', 'impulsivity'])
    elif diagnosis == 'combination':
        res = find_appropriate_suppliments(['hyperactivity', 'impulsivity', 'combination'])
    else:
        return diagnosis

    for entry in res:
        relief = 40 * entry['improvement']
        relief = round(relief, 2)
        supplements.append(
            {'name': entry['name'], 'dosage': entry['dosage'], 'relief': relief, 'improved_symptom': entry['symptom'],
             'type': entry['type']})

    sports = set()
    for symptom in symptoms:
        temp = map[symptom]
        for i in temp:
            sports.add(i)

    return {'diagnosis': diagnosis, 'supplements': supplements, 'sports': sports}  # noqa


def get_diagnosis(symptoms):
    """
        Determines the diagnosis based on the provided symptoms.

        The function first converts the symptoms into a set for easier comparison.
        It counts the number of symptoms related to inattention and hyperactivity using set intersections.

        If the count of both inattention and hyperactivity symptoms is less than 6, it returns 'No diagnosis'.
        If the count of inattention symptoms is greater than or equal to 6 and greater than the count of hyperactivity
        symptoms, it returns 'inattention'.
        If the count of inattention symptoms is less than 6 and greater than or equal to the count of hyperactivity symptoms,
        it returns 'hyperactivity/impulsivity'.
        Otherwise, it returns 'combination'.

        Args:
            symptoms (list): A list of symptoms.

        Returns:
            A string representing the diagnosis.

    """
    symptom_set = set(symptoms)

    inattention_count = len(INATTENTION.intersection(symptom_set))
    hyperactivity_count = len(HYPERACTIVITY.intersection(symptom_set))
    if inattention_count < 6 and hyperactivity_count<6:
        return 'No diagnosis'
    if inattention_count >= 6 > hyperactivity_count:
        return "inattention"
    elif inattention_count < 6 <= hyperactivity_count:
        return "hyperactivity/impulsivity"
    else:
        return "combination"


def get_programm_as_string(id, name, data):
    """
         Generates a string representation of an ADHD treatment program to be inserted into DB.
    Args:
        id (str): The ID of the program.
        name (str): The name associated with the program.
        data (dict): A dictionary containing program data, including diagnosis, supplements, and sports activities.

    Returns:
        A tuple containing the program string and a set of sports activities.
    Example: ADHD treatment program for:

             Name: Yosi Biton
             ID: 12478

             Recommendations:
             Diagnosis: inattention

             Nutritional Supplements:
             - iron: 10 mg/day. Expected improvement in inattention is: 36.8
             - EFAs: 1.8 grams of total omega-3/day. Expected improvement in inattention is: 19.2
             - pycnogenol: 1-2 pills. Expected improvement in inattention is: 40.0
             - Ningdong: 5 mg/day. Expected improvement in inattention is: 23.6

             Sports Activities:
              Aerobics
                On Monday
              Martial arts
                On Wednesday

    """
    result_string = "ADHD treatment program for:\n\nName: {name}\nID: {id}\n\nRecommendations:\nDiagnosis: {dagnosis}\n\n"  # Nutritional Supplements:\n- {Supplement}: {Dosage}\n\t- {Description}\n\n"

    result_string = result_string.replace('{name}', name)
    result_string = result_string.replace('{id}', id)
    result_string = result_string.replace('{dagnosis}', data['diagnosis'])

    result_string += 'Nutritional Supplements:\n'

    for supplement in data['supplements']:
        result_string += '- ' + supplement['name']
        result_string += ': ' + supplement['dosage'] + '. Expected improvement in ' + supplement[
            'improved_symptom'] + ' is: ' + str(
            supplement['relief']) + '\n'

    result_string += '\nSports Activities:\n'

    return result_string, data['sports']


def strint_to_dict(string):
    """
        Converts a string representation of sports activities into a list of sports.

        Args:
            string (str): The string representation of sports activities.

        Returns:
            A list of sports activities extracted from the input string.
    """
    sports = ['Dance/Yoga', 'Aerobics', 'Martial arts', 'Team Games']

    substring = string.split("Sports Activities:\n", 1)[1]
    res = []
    for sport in sports:
        if sport in substring:
            res.append(sport)
    return res


def find_appropriate_suppliments(symptoms):
    """
        Finds appropriate supplements based on the given symptoms.

        Args:
            symptoms (list): A list of symptoms.

        Returns:
            A list of dictionaries representing the appropriate supplements.
    """
    query = "SELECT * FROM nutritions"
    nutrients_table = db.execute_query(query)

    query = "SELECT * FROM nutrition_relief"
    improvement_table = db.execute_query(query)

    supplements = []

    for entry in improvement_table:
        symptom = entry['symptom'].lower()
        if any(symptom.lower() in s.lower() for s in symptoms):
            supplement_name = entry['name']
            improvement = entry['efficiency']
            supplement_details = [supplement for supplement in nutrients_table if
                                  supplement['name'] == supplement_name][0]

            supplement = {
                'name': supplement_details['name'],
                'dosage': supplement_details['dose'],
                'type': supplement_details['type'],
                'improvement': improvement,
                'symptom': symptom
            }

            supplements.append(supplement)

    return supplements


def remove_duplicates(data: list):
    """
    Removes duplicates from a supplements list based on the 'name' field.

    Args:
        data (list): A list of dictionaries.

    Returns:
        A new list with duplicates removed.
    """
    for i, candidate in enumerate(data):
        for item in data[i + 1:]:
            if candidate['name'] == item['name']:
                if candidate['dosage'] < item['dosage']:
                    data.remove(candidate)
                else:
                    data.remove(item)
    return data


if __name__ == '__main__':
    # from openAI import OpenAIModel
    #
    # url = 'https://api.openai.com/v1/chat/completions'
    # # api_key = os.environ.get("ENV_API_KEY")
    # api_key = "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"
    # chat = OpenAIModel(api_key, url)
    # res = find_appropriate_suppliments(['hyperactivity', 'impulsivity', 'inattention'])
    # res = remove_duplicates(res)
    # rec = chat.execute_query(res)
    # print(res)
    re = get_program(['RUNNINGCLIMBING',
                      'UNQUIET',
                      'DRIVENMOTOR'
                      'EXCESSIVETALK',
                      'BLURTING',
                      'IMPATIENT',
                      'INTRUDES'])
