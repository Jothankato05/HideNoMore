# Hide No More

[![Release](https://github.com/Jothankato05/HideNoMore/actions/workflows/release.yml/badge.svg)](https://github.com/Jothankato05/HideNoMore/actions/workflows/release.yml)
[![GitHub stars](https://img.shields.io/github/stars/Jothankato05/HideNoMore?style=social)](https://github.com/Jothankato05/HideNoMore/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Stealthy, modular OSINT CLI tool for phone, username, metadata, domain/IP, and geolocation reconnaissance.

## Project Board

Track features, bugs, and ideas on the [Hide No More Development Board](https://github.com/users/Jothankato05/projects/1).

## Contributing

Contributions are welcome! Please open an issue or pull request. Use the provided templates for bug reports and feature requests.

## Automated Releases & Changelog

- Releases are created automatically when you push a tag like `v1.0.0`.
- Changelog is generated automatically on release.

## Usage

```bash
python hide_no_more.py phone +2348061234567
python hide_no_more.py username john_doe
python hide_no_more.py metadata somefile.jpg
python hide_no_more.py domain example.com
python hide_no_more.py shodan 8.8.8.8
```

## Setup

### Recommended: Use a Virtual Environment

#### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows (CMD)
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

2. For metadata extraction, install [ExifTool](https://exiftool.org/) on your system.
3. Configure API keys in `config/config.json` as needed.

## Extending

1. Add new modules in `modules/` and import them in `hide_no_more.py`.
2. Ready for Shodan, proxy, and more integrations.

```bash
python hide_no_more.py metadata somefile.jpg
python hide_no_more.py domain example.com
python hide_no_more.py shodan 8.8.8.8
```
