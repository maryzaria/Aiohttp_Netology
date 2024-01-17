import requests

#
# response = requests.post("http://127.0.0.1:8080/user",
#                         json={"name": "user_1", "password": "1234"},
#                         )
#
# print(response.status_code)
# print(response.text)


# response = requests.get("http://127.0.0.1:8080/user/1",
#
#                         )
#
# print(response.status_code)
# print(response.text)


# response = requests.patch("http://127.0.0.1:8080/user/1",
#                         json={"name": "new_user_name"},
#                         )
#
# print(response.status_code)
# print(response.text)


# response = requests.delete("http://127.0.0.1:8080/user/1")
#
# print(response.status_code)
# print(response.text)


response = requests.get(
    "http://127.0.0.1:8080/user/1",
)

print(response.status_code)
print(response.text)
