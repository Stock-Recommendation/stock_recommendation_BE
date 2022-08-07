import requests

endpoint = "http://localhost:8000/api/products/1/update/" #http://127.0.0.1:8000/
# endpoint = "http://localhost:8000/api/carts/1" #http://127.0.0.1:8000/

data = {
    "title":"this field is done",
    "price": 100,
}
get_response = requests.put(endpoint, json=data)
print(get_response.json())