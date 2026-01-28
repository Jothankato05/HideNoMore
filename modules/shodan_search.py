import requests
import json
import os

import sys

def search(target):
    """
    Search Shodan for information about an IP or domain.
    Requires SHODAN API key in config.json (same directory as executable) or config/config.json.
    """
    print(f"[Shodan] Searching for: {target}")
    
    # Determine base path
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        # Parent of modules directory
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Try multiple config locations
    possible_paths = [
        os.path.join(base_path, 'config.json'),
        os.path.join(base_path, 'config', 'config.json')
    ]
    
    config_path = None
    for p in possible_paths:
        if os.path.exists(p):
            config_path = p
            break
            
    api_key = None
    if config_path:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            api_key = config.get('shodan_api_key')
        except Exception as e:
            print(f"[!] Failed to load config from {config_path}: {e}")
    
    if not api_key or api_key == 'YOUR_SHODAN_API_KEY_HERE':
        print(f"[!] Shodan API key not found.")
        print(f"[!] Please create a 'config.json' file in {base_path} with: {{ \"shodan_api_key\": \"YOUR_KEY\" }}")
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
