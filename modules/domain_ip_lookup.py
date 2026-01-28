import whois

def lookup(domain):
    print(f"Performing Whois lookup on {domain}...")
    try:
        domain_info = whois.whois(domain)
        for key, value in domain_info.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error looking up {domain}: {str(e)}")
