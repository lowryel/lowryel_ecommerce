print('hello')
import requests


url = "https://d7sms.p.rapidapi.com/secure/send"

payload = "{\r\n    \"coding\": \"8\",\r\n    \"from\": \"SMSInfo\",\r\n    \"hex-content\": \"00480065006c006c006f\",\r\n    \"to\": 971562316353\r\n}"
headers = {
    'content-type': "application/json",
    'authorization': "undefined",
    'x-rapidapi-host': "d7sms.p.rapidapi.com",
    'x-rapidapi-key': "7436e1b2bbmsh0a38a56fd7e9989p1befaajsn4ee97f0f4434"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
