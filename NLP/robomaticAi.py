import requests

url = "https://robomatic-ai.p.rapidapi.com/api"

def chat(name, text, key):
  payload = {
    "in": f'(name:{name})' + text,
    "op": "in",
    "cbot": "1",
    "SessionID": "RapidAPI1",
    "cbid": "1",
    "key": "RHMN5hnQ4wTYZBGCF3dfxzypt68rVP",
    "ChatSource": "RapidAPI",
    "duration": "1"
  }
  headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": key,
    "X-RapidAPI-Host": "robomatic-ai.p.rapidapi.com"
  }

  response = requests.post(url, data=payload, headers=headers)
  printed = response.json()#['out']
  print("0001")

  return printed['out']