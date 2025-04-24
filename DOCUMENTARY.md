# Hide No More Documentary

## Introduction

**Hide No More** is a stealthy, modular OSINT CLI tool created by Jothan Jerry Kato (aka Jothan Prime), CEO of Primers Organization and an ethical hacker. It empowers security researchers and investigators to perform deep, multi-source intelligence gathering from the command line.

---

## Author & Credits
- **Author:** Jothan Jerry Kato (Jothan Prime)
- **Contact:** 09028178661, jerryjothan639@gmail.com
- **Organization:** Primers Organization
- **Role:** CEO, Ethical Hacker

---

## Vision & Purpose

"Hide No More" was built to:
- Provide a single, extensible CLI for OSINT tasks
- Help ethical hackers, journalists, and investigators gather intelligence efficiently
- Encourage responsible, lawful use of open-source intelligence

---

## Features
- **Phone Number Lookup**: Carrier, region, and validity checks
- **Username Search**: Checks username presence on major social platforms
- **Metadata Extraction**: Extracts metadata from images and documents using ExifTool
- **Domain/IP Search**: Whois, DNS, and reverse lookups
- **Geolocation Tracing**: Traces geolocation from IPs/domains
- **Shodan Integration**: Advanced IP/domain intelligence via Shodan API

---

## Usage Example
```bash
python hide_no_more.py phone +2348061234567
python hide_no_more.py username john_doe
python hide_no_more.py metadata somefile.jpg
python hide_no_more.py domain example.com
python hide_no_more.py geo 8.8.8.8
python hide_no_more.py shodan 8.8.8.8
```

---

## Extensibility
- Add new modules in `modules/` for more OSINT sources
- Ready for proxy support, more APIs, and custom automation

---

## Ethical Notice
This tool is intended for ethical, legal use only. Always respect privacy, terms of service, and local laws. The author and contributors are not responsible for misuse.

---

## Contact
For support, features, or collaboration:
- Email: jerryjothan639@gmail.com
- Phone: 09028178661
- GitHub: [your future repo link here]

---

## About the Author
Jothan Jerry Kato (Jothan Prime) is a passionate ethical hacker, educator, and CEO of Primers Organization, committed to advancing cybersecurity awareness and responsible hacking.
