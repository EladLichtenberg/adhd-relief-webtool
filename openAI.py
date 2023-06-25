import openai
import requests
import os
import json

class OpenAIModel:

    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url

    def execute_query(self, data: list):
        """
        Executes a query to the openAI API using the provided data - supplements with dosage.

        Args:
            data (list): A list of dictionaries containing the query data.

        Returns:
            content (str): Recomendations containig the menu for a day, that contains required supplements in certain dasage
        """
        token = "Bearer " + self.api_key

        header = {"Content-Type": "application/json",
                  "Authorization": token}

        content = f"""Give me menu for per day that consists: """
        for item in data:
            if item['type'] == 'Nutrients':
                content += item['dosage'] + ' ' + item['name'] + '\n'

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": content}]
        }

        response = requests.post(url=self.url, headers=header, json=data)
        response = response.json()
        content = response['choices'][0]['message']['content']
        content += '\n\nNote: This menu is a general guideline and may not meet individual dietary needs. It is always a good idea to consult with a healthcare professional or a registered dietitian for personalized dietary recommendations.\n'

        print(json.dumps(response, indent=4))
        print(content)
        return content

