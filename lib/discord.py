import requests
import settings as settings

def send(message):
  url = settings.get('discord')[1]
  if url:
    requests.post(url, data = {"content":message, "username":"GazelleUI", "avatar_url":"https://xanderstrike.com/gazelleui.png"})
