import os
import requests
import zipfile
from datetime import datetime
import time
import sys
import re
import json

# Define the default config
DEFAULT_CONFIG = {
    "rate_limiting": True
}

def load_config(config_path='config.json'):
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config, config_path='config.json'):
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def print_progress_bar(downloaded, total):
    bar_length = 60  # Length of the progress bar
    progress = (downloaded / total) if total else 0  # Progress as a fraction
    filled_length = int(round(bar_length * progress))
    percent = round(100.0 * progress, 1)
    
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percent}% {downloaded / (1024 * 1024):.2f} MiB')
    sys.stdout.flush()

def download_with_progress(url, path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kilobyte

    if total_size == 0:
        print("Total size could not be determined.")
        total_size = None

    downloaded = 0
    start_time = time.time()

    with open(path, 'wb') as f:
        for data in response.iter_content(block_size):
            downloaded += len(data)
            f.write(data)

            # Update progress every second
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= 1:
                print_progress_bar(downloaded, total_size)
                start_time = current_time  # Reset start time for the next update

    # Finish progress bar
    sys.stdout.write('\r[' + '#' * 60 + '] 100% {0:.2f} MiB\n'.format(downloaded / (1024 * 1024)))
    sys.stdout.flush()

def check_repo_url_valid(repo_url):
    # Check if the URL is a valid GitHub repository URL
    github_pattern = re.compile(r'https://github\.com/[^/]+/[^/]+')
    if not github_pattern.match(repo_url):
        return False

    # Check if the repository actually exists
    repo_api_url = repo_url.replace('https://github.com/', 'https://api.github.com/repos/')
    response = requests.get(repo_api_url)
    return response.status_code == 200

def download_github_repo(repo_url):
    if not check_repo_url_valid(repo_url):
        print("The provided repository URL is invalid or does not exist.")
        return False
    else:
        return True

def apply_rate_limit(session):
    config = load_config()
    if config.get("rate_limiting", True):
        session.headers.update({'X-RateLimit-Limit': '5000'})
        session.headers.update({'X-RateLimit-Remaining': '5000'})
        session.headers.update({'X-RateLimit-Reset': str(int(time.time()) + 3600)})

if __name__ == "__main__":
    config = load_config()

    # Ensure rate limiting is enabled if not already set
    if "rate_limiting" not in config:
        save_config(DEFAULT_CONFIG)
        config = DEFAULT_CONFIG

    while True:
        repo_url = input("Enter the GitHub repository URL: ")
        if download_github_repo(repo_url):
            break

    repo_name = repo_url.rstrip('/').split('/')[-1]
    repo_owner = repo_url.split('/')[-2]
    current_date = datetime.now().strftime('%Y-%m-%d')
    repo_folder = f"{repo_name}_{current_date}"

    # Create a directory with the repository's name and current date
    if not os.path.exists(repo_folder):
        os.makedirs(repo_folder)

    # Create a directory for releases within the repository folder
    releases_folder = os.path.join(repo_folder, "Releases")
    if not os.path.exists(releases_folder):
        os.makedirs(releases_folder)

    # Create the archive information file first
    archive_info_path = os.path.join(repo_folder, "archive-information.txt")

    # Get the repository's API URL
    repo_api_url = repo_url.replace('https://github.com/', 'https://api.github.com/repos/')

    # Initialize information for the archive file
    owner_name = "Unknown"
    license_info = "No license information available"
    release_date = "N/A"

    # Set up session with rate limiting if enabled
    session = requests.Session()
    apply_rate_limit(session)

    # Get the repository information
    repo_info_response = session.get(repo_api_url)
    if repo_info_response.status_code == 200:
        repo_info = repo_info_response.json()
        owner_name = repo_info['owner']['login']
        license_info = repo_info['license']['name'] if repo_info['license'] else "No license information available"
    else:
        print(f"Failed to get repository information: {repo_info_response.status_code}")

    # Get the latest release information
    latest_release_api_url = f"{repo_api_url}/releases/latest"
    latest_release_response = session.get(latest_release_api_url)
    if latest_release_response.status_code == 200:
        latest_release = latest_release_response.json()
        release_date = latest_release['published_at']
    else:
        print(f"Failed to get latest release: {latest_release_response.status_code}")

    # Create the archive information file
    with open(archive_info_path, 'w') as f:
        f.write(f"Repository: {repo_name}\n")
        f.write(f"Owner: {owner_name}\n")
        f.write(f"Repository URL: {repo_url}\n")
        f.write(f"Archive Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Latest Release Date: {datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S') if release_date != 'N/A' else 'N/A'}\n")
        f.write(f"License: {license_info}\n")

    print(f"\nCreated archive information file at {archive_info_path}")

    # Define the path for the source code zip file
    source_zip_path = os.path.join(repo_folder, f"{repo_name}-source.zip")
    
    # URL for downloading the source code zip
    source_zip_url = f"{repo_api_url}/zipball/master"
    
    # Attempt to download the source code zip file
    print(f"Downloading source code to {source_zip_path}...")
    download_with_progress(source_zip_url, source_zip_path)

    # Initialize flag for zip file validity
    zip_file_valid = False

    # Validate the downloaded zip file
    try:
        with zipfile.ZipFile(source_zip_path, 'r') as zip_ref:
            zip_file_valid = True
    except zipfile.BadZipFile:
        print(f"\nThe downloaded zip file is not valid. Trying alternative download URL.")
        zip_file_valid = False

    # Attempt to download from the alternative URL if the zip file is invalid
    if not zip_file_valid:
        alternative_zip_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/master.zip"
        print(f"Attempting alternative download from {alternative_zip_url}...")
        download_with_progress(alternative_zip_url, source_zip_path)

        # Validate the downloaded zip file again
        try:
            with zipfile.ZipFile(source_zip_path, 'r') as zip_ref:
                zip_file_valid = True
        except zipfile.BadZipFile:
            print(f"\nThe alternative zip file is also not valid. Skipping extraction.")
            zip_file_valid = False

    # Proceed with extraction if the zip file is valid
    if zip_file_valid:
        try:
            with zipfile.ZipFile(source_zip_path, 'r') as zip_ref:
                zip_ref.extractall(repo_folder)
            print(f"\nExtracted source code to {repo_folder}")
        except Exception as e:
            print(f"Failed to extract zip file: {e}")
    else:
        # Remove the invalid zip file if it's not valid
        if os.path.exists(source_zip_path):
            os.remove(source_zip_path)

    # Download latest release assets if there are any
    if release_date != "N/A":
        for asset in latest_release['assets']:
            asset_url = asset['browser_download_url']
            asset_name = asset['name']
            asset_path = os.path.join(releases_folder, asset_name)
            print(f"\nDownloading latest release asset {asset_name} to {asset_path}...")
            download_with_progress(asset_url, asset_path)

    print("\nScript execution completed.")

