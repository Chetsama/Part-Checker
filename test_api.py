import requests

from auth.auth import password, username

# Test direct API call with debugging info
payload = {
    "source": "amazon_search",
    "query": "RTX5070",
    "geo_location": "GB",
    "parse": True,
}

print(f"Username: {username}")
print(f"Password: {password}")

try:
    print(payload)
    r = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(str(username), str(password)),
        json=payload,
        timeout=30,
    )

    print(f"Status code: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type')}")
    print(f"Response text preview: {r.text[:200]}...")

except Exception as e:
    print(f"Error making request: {e}")
