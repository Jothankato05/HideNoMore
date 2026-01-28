import requests

def trace(target):
    # Colors
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    print(f"{CYAN}Tracing geolocation for {target}...{RESET}")
    try:
        response = requests.get(f'https://ipinfo.io/{target}/json')
        if response.status_code != 200:
            print(f"{RED}Error: Received status code {response.status_code}{RESET}")
            return

        data = response.json()
        if 'error' in data:
            print(f"{RED}API Error: {data['error'].get('message', 'Unknown error')}{RESET}")
            return

        ip = data.get('ip', 'N/A')
        city = data.get('city', 'N/A')
        region = data.get('region', 'N/A')
        country = data.get('country', 'N/A')
        loc = data.get('loc', 'N/A')
        org = data.get('org', 'N/A')
        timezone = data.get('timezone', 'N/A')

        print(f"{BOLD}IP:{RESET} {GREEN}{ip}{RESET}")
        print(f"{BOLD}Location:{RESET} {GREEN}{city}, {region}, {country}{RESET}")
        print(f"{BOLD}Coordinates:{RESET} {GREEN}{loc}{RESET}")
        print(f"{BOLD}Organization:{RESET} {GREEN}{org}{RESET}")
        print(f"{BOLD}Timezone:{RESET} {GREEN}{timezone}{RESET}")

        if loc != 'N/A':
            print(f"{BOLD}Google Maps:{RESET} {CYAN}https://www.google.com/maps/place/{loc}{RESET}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}Error tracing {target}: {str(e)}{RESET}")
