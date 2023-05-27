import openai
import requests
import os
import json

url = 'https://api.openai.com/v1/chat/completions'

api_key = ""
token = "Bearer " + api_key

header = {"Content-Type": "application/json",
          "Authorization": token}
data = {
  "model": "davinci",
  "messages": [{"role": "user", "content": "Hello!"}]
}
response = requests.post(url=url, headers=header, json=data)
print(json.dumps(response.json(), indent=4))
