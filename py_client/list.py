import requests

endpoint = "http://localhost:8000/api/stocks/" #http://127.0.0.1:8000/
# endpoint = "http://localhost:8000/api/carts/1" #http://127.0.0.1:8000/

data = {
    "title":"this field is done",
    "price": 1200,
}
get_response = requests.get(endpoint, json=data)
print(get_response.json())
