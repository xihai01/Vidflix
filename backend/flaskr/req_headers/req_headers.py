import os

def req_header():
  headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + os.getenv('API_KEY')
  }

  return headers
