import requests

def map_ip(ip_or_domain):
    """
    Get geolocation for IP/domain and print a map link.
    """
    print(f"[IP by Map] Locating: {ip_or_domain}")
    try:
        response = requests.get(f'https://ipinfo.io/{ip_or_domain}/json')
        data = response.json()
        loc = data.get('loc')
        if loc:
            lat, lon = loc.split(',')
            print(f"Latitude: {lat}\nLongitude: {lon}")
            print(f"Google Maps: https://www.google.com/maps?q={lat},{lon}")
            print(f"OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}")
        else:
            print("Could not determine location for this IP/domain.")
    except Exception as e:
        print(f"Error: {e}")
