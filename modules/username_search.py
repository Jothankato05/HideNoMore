import requests

def search(username):
    print(f"[Username Search] Searching for username: {username}")
    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Facebook": f"https://facebook.com/{username}"
    }
    headers = {"User-Agent": "Mozilla/5.0 (compatible; HideNoMore/1.0)"}
    for platform, url in platforms.items():
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                print(f"[+] Found on {platform}: {url}")
            elif resp.status_code == 404:
                print(f"[-] Not found on {platform}")
            else:
                print(f"[?] {platform} returned status {resp.status_code}")
        except requests.RequestException as e:
            print(f"[!] Error checking {platform}: {e}")
