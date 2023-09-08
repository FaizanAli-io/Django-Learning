import requests

endpoint = "http://localhost:8000/api/"

response = requests.post(
    endpoint,
    json={
        "title": "Slim Shady",
        "content": "Hello World",
    },
)

print(response.json())
