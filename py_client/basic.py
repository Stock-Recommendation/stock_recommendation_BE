import requests

# endpoint = "https://httpbin.org/status/200/"
# endpoint = "https://httpbin.org/"
endpoint = "http://localhost:8000/" #http://127.0.0.1:8000/
get_response = requests.get(endpoint)
print(get_response.text)