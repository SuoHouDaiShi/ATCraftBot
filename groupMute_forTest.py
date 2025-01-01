import http.client
import json

conn = http.client.HTTPConnection("localhost", 53234)
payload = json.dumps({
    "group_id": 805950688,
    "enable": True
})
headers = {
    'Content-Type': 'application/json'
}
conn.request("POST", "/set_group_whole_ban", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))