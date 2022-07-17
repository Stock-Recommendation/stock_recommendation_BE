import requests

id = input("what is the product id?")
try:
    id = int(id)
except:
    print('fuck off')
    
if id:
    endpoint = f"http://localhost:8000/api/products/{id}/delete/" #http://127.0.0.1:8000/
    get_response = requests.delete(endpoint)
    print(get_response.status_code, get_response.status_code==204)