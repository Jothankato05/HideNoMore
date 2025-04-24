import requests
import time

def live_track(ip_or_domain, interval=10):
    """
    Continuously fetch and print geolocation for an IP/domain every interval seconds.
    """
    print(f"[Live Tracking] Tracking: {ip_or_domain} (updates every {interval} seconds, Ctrl+C to stop)")
    try:
        while True:
            response = requests.get(f'https://ipinfo.io/{ip_or_domain}/json')
            data = response.json()
            loc = data.get('loc')
            if loc:
                lat, lon = loc.split(',')
                print(f"\nLatitude: {lat}\nLongitude: {lon}")
                print(f"Google Maps: https://www.google.com/maps?q={lat},{lon}")
                print(f"OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=12/{lat}/{lon}")
            else:
                print("Could not determine location for this IP/domain.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nLive tracking stopped.")
