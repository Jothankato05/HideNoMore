import requests
import json
import os

def search(target):
    """
    Search Shodan for information about an IP or domain.
    Requires SHODAN API key in config/config.json.
    """
    print(f"[Shodan] Searching for: {target}")
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        api_key = config.get('shodan_api_key')
        if not api_key or api_key == 'YOUR_SHODAN_API_KEY_HERE':
            print("[!] Shodan API key not set in config/config.json")
            return
    except Exception as e:
        print(f"[!] Failed to load config: {e}")
        return
    url = f"https://api.shodan.io/shodan/host/{target}?key={api_key}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"[!] Shodan Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"[!] Shodan request failed: {e}")
