import argparse
import os
from modules import phone_lookup, username_search, metadata_extractor, domain_ip_lookup, geolocation, shodan_search, ip_by_map, live_tracking

def banner():
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    # ASCII Art
    print(rf"""
{BOLD}{RED} _    _ _     _     _      _   _           _                {RESET}{CYAN}      .     
{BOLD}{RED}| |  | (_)   | |   | |    | | | |         | |               {RESET}{CYAN}     / V\   
{BOLD}{RED}| |__| |_  __| | __| | ___| |_| |__   ___ | |_ ___  ___ ___ {RESET}{CYAN}    / `  /  
{BOLD}{RED}|  __  | |/ _` |/ _` |/ _ \ __| '_ \ / _ \| __/ _ \/ __/ __|{RESET}{CYAN}   <<   |   
{BOLD}{RED}| |  | | | (_| | (_| |  __/ |_| | | | (_) | ||  __/\__ \__ \{RESET}{CYAN}   /    |   
{BOLD}{RED}|_|  |_|_|\__,_|\__,_|\___|\__|_| |_|\___/ \__\___||___/___/{RESET}{CYAN}  /_    |   
{CYAN}      `   `
{RESET}""")
    print(f"{CYAN}{BOLD}By Jothan Prime{RESET}\n")
    print(f"{YELLOW}{BOLD}Stealthy, Fast, Reliable OSINT Recon Tool{RESET}")
    print(f"{CYAN}{'-'*60}{RESET}")

def main():
    banner()
    while True:
        RED = '\033[91m'
        GREEN = '\033[92m'
        CYAN = '\033[96m'
        YELLOW = '\033[93m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        print(f"""
{YELLOW}{BOLD}[1]{RESET} {CYAN}Phone Lookup{RESET}

{YELLOW}{BOLD}[2]{RESET} {CYAN}Username Search{RESET}

{YELLOW}{BOLD}[3]{RESET} {CYAN}Metadata Extraction{RESET}

{YELLOW}{BOLD}[4]{RESET} {CYAN}Domain/IP Lookup{RESET}

{YELLOW}{BOLD}[5]{RESET} {CYAN}Geolocation Trace{RESET}

{YELLOW}{BOLD}[6]{RESET} {CYAN}Shodan Search{RESET}

{YELLOW}{BOLD}[7]{RESET} {GREEN}Update Tool{RESET}

{YELLOW}{BOLD}[8]{RESET} {CYAN}IP by Map{RESET}

{YELLOW}{BOLD}[9]{RESET} {CYAN}Live Tracking{RESET}

{YELLOW}{BOLD}[99]{RESET} {RED}About{RESET}

{YELLOW}{BOLD}[0]{RESET} {RED}Exit{RESET}
""")
        try:
            choice = input(f"{GREEN}{BOLD}Select an option: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}Exiting. Goodbye!{RESET}")
            break
        if choice == "1":
            number = input(f"{CYAN}Enter phone number: {RESET}").strip()
            phone_lookup.lookup(number)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "2":
            username = input(f"{CYAN}Enter username: {RESET}").strip()
            username_search.search(username)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "3":
            file_path = input(f"{CYAN}Enter file path: {RESET}").strip()
            metadata_extractor.extract(file_path)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "4":
            target = input(f"{CYAN}Enter domain or IP: {RESET}").strip()
            domain_ip_lookup.lookup(target)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "5":
            target = input(f"{CYAN}Enter IP or domain: {RESET}").strip()
            geolocation.trace(target)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "6":
            target = input(f"{CYAN}Enter IP or domain for Shodan: {RESET}").strip()
            shodan_search.search(target)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "7":
            import subprocess
            print(f"{YELLOW}Updating Hide No More...{RESET}")
            try:
                result = subprocess.run(["git", "pull"], capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print(f"{RED}{result.stderr}{RESET}")
                print(f"{GREEN}Update complete! Restart the tool if necessary.{RESET}")
            except Exception as e:
                print(f"{RED}Update failed: {e}{RESET}")
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "8":
            ip_or_domain = input(f"{CYAN}Enter IP or domain: {RESET}").strip()
            ip_by_map.map_ip(ip_or_domain)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "9":
            ip_or_domain = input(f"{CYAN}Enter IP or domain: {RESET}").strip()
            interval = input(f"{CYAN}Enter update interval in seconds (default 10): {RESET}").strip()
            try:
                interval = int(interval) if interval else 10
            except ValueError:
                interval = 10
            live_tracking.live_track(ip_or_domain, interval)
            print(f"\n{GREEN}Task complete. Please rerun the tool to start again.{RESET}")
            break
        elif choice == "99":
            print(f"\n{BOLD}{CYAN}Hide No More - OSINT Tool\nBy Jothan Prime\nStealthy, Fast, Reliable OSINT Recon{RESET}\n")
        elif choice == "0":
            print(f"{RED}Exiting. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid option. Please try again.{RESET}")

if __name__ == "__main__":
    main()
