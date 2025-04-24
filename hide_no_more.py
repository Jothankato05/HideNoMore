import argparse
import os
from modules import phone_lookup, username_search, metadata_extractor, domain_ip_lookup, geolocation, shodan_search

def banner():
    print("""
    ---------------------------------------------------
    |  Hide No More - OSINT Tool                      |
    |  v1.0 - Stealthy, Fast, Reliable OSINT Recon    |
    ---------------------------------------------------
    """)

def parse_args():
    parser = argparse.ArgumentParser(description="Hide No More - OSINT Recon Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Phone lookup
    phone_parser = subparsers.add_parser("phone", help="Lookup information based on phone number")
    phone_parser.add_argument("number", help="Phone number to search")
    
    # Username search
    user_parser = subparsers.add_parser("username", help="Search for social media profiles based on username")
    user_parser.add_argument("username", help="Username to search")
    
    # Metadata extraction
    meta_parser = subparsers.add_parser("metadata", help="Extract metadata from files")
    meta_parser.add_argument("file", help="File path to extract metadata from")

    # Domain/IP lookup
    domain_parser = subparsers.add_parser("domain", help="Lookup domain or IP information")
    domain_parser.add_argument("target", help="Domain or IP to look up")

    # Geolocation trace
    geo_parser = subparsers.add_parser("geo", help="Trace geolocation data")
    geo_parser.add_argument("target", help="IP address or domain to trace")

    # Shodan search
    shodan_parser = subparsers.add_parser("shodan", help="Search Shodan for IP/domain intelligence")
    shodan_parser.add_argument("target", help="IP address or domain to search on Shodan")

    return parser.parse_args()

def main():
    args = parse_args()
    banner()

    if args.command == "phone":
        phone_lookup.lookup(args.number)
    elif args.command == "username":
        username_search.search(args.username)
    elif args.command == "metadata":
        metadata_extractor.extract(args.file)
    elif args.command == "domain":
        domain_ip_lookup.lookup(args.target)
    elif args.command == "geo":
        geolocation.trace(args.target)
    elif args.command == "shodan":
        shodan_search.search(args.target)
    else:
        print("Invalid command. Use --help for usage.")

if __name__ == "__main__":
    main()
