import requests

def trace(target):
    print(f"Tracing geolocation for {target}...")
    try:
        response = requests.get(f'https://ipinfo.io/{target}/json')
        data = response.json()
        print(f"IP: {data.get('ip')}")
        print(f"Location: {data.get('city')}, {data.get('region')}, {data.get('country')}")
    except requests.exceptions.RequestException as e:
        print(f"Error tracing {target}: {str(e)}")
