import requests

# endpoint = "http://localhost:8000/api/products/1" #http://127.0.0.1:8000/
endpoint = "http://localhost:8000/api/carts/1" #http://127.0.0.1:8000/

get_response = requests.get(endpoint, params={'abc':12}, json={"query": "hello shit"})
print(get_response.json())