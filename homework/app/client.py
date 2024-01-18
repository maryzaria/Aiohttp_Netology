import requests

response = requests.post(
    "http://127.0.0.1:8080/advert",
    json={
        "title": "Test advertisement",
        "description": "some test advertisement",
        "owner": "mary",
    },
)

# response = requests.get("http://127.0.0.1:8080/advert/1")

# response = requests.patch("http://127.0.0.1:8080/advert",
#                           json={
#                              "title": "New name",
#                              "description": "some test advertisement",
#                              "owner": "Mary"
#                           },
#                           )

# response = requests.delete("http://127.0.0.1:8080/advert/4")

print(response.status_code)
print(response.text)
