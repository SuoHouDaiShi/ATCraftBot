import http.client
import json

conn = http.client.HTTPConnection("localhost", 53234)
payload = json.dumps({
    "group_id": 0,
    "user_id": 0
})
headers = {
    'Content-Type': 'application/json'
}
conn.request("POST", "/group_poke", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))