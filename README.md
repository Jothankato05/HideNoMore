# Hide No More

Stealthy, modular OSINT CLI tool for phone, username, metadata, domain/IP, and geolocation reconnaissance.

## Usage

```bash
python hide_no_more.py phone +2348061234567
python hide_no_more.py username john_doe
python hide_no_more.py metadata somefile.jpg
python hide_no_more.py domain example.com
python hide_no_more.py geo 8.8.8.8
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. For metadata extraction, install [ExifTool](https://exiftool.org/) on your system.
3. Configure API keys in `config/config.json` as needed.

## Extending
- Add new modules in `modules/` and import them in `hide_no_more.py`.
- Ready for Shodan, proxy, and more integrations.
