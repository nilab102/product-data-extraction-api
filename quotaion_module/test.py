
import requests
import sys


# API endpoint URL
url = "http://127.0.0.1:9100/email_router2/search"  # Update with your actual API URL

# Request payload
payload = {
    "query": "Sony Bravia wholesaler contact email in saudia arab",
}


print("Sending request to API...")
response = requests.post(url, json=payload, stream=True)

print(f"Status code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print("Raw response:")

for chunk in response.iter_content(chunk_size=1):
    if chunk:
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()


#curl -N -X POST http://176.9.16.194:9100/price_router2/search -H "Content-Type: application/json" -d "{\"query\": \"Sony Bravia 55-inch 4K UHD Smart LED TV\"}"
#curl -N -X POST http://176.9.16.194:9100/email_router2/search -H "Content-Type: application/json" -d "{\"query\": \"cisco router wholesaler email addresss in saudi arab\"}"