import requests

API_BASE = "https://covid-api.com/api"

def fetch_regions():
    url = f"{API_BASE}/regions"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # check HTTP status
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None

if __name__ == "__main__":
    regions = fetch_regions()
    if regions:
        print(f"Fetched {len(regions['data'])} regions")
        # Print first 5 regions as a sample
        for region in regions['data'][:5]:
            print(region['name'], region['iso'])
