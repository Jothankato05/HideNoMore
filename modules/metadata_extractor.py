import subprocess

def extract(file_path):
    print(f"Extracting metadata from {file_path}...")
    try:
        result = subprocess.run(['exiftool', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except FileNotFoundError:
        print("ExifTool not found. Please install it.")
