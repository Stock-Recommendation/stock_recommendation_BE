import requests

# endpoint = "https://httpbin.org/status/200/"
# endpoint = "https://httpbin.org/"
endpoint = "http://localhost:8000/api/" #http://127.0.0.1:8000/
get_response = requests.post(endpoint, params={'abc':12}, json={"query": "hello shit"})

print(get_response.json())