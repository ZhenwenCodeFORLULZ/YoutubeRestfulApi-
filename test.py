import requests
BASE = "http://127.0.0.1:5000/" #location of the API and the server its running on
data = [
    {"likes":78,"name": "Joe","views":1000000},
    {"likes":100000,"name": "How to make Rest API","views":8000000},
    {"likes":35,"name": "Zhen","views":2000}
]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

#response = requests.put(BASE + "video/1",{"likes":10,"name": " Tim","views":1000000})
response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.get(BASE + "video/6")
print(response.json())
response = requests.patch(BASE + "video/2",{"views":99,"likes":101})
print(response.json())

response = requests.patch(BASE + "video/2",{"views":100,"likes":101})
print(response.json())