# RepositoryArchiveScript

A Python script designed to easily download the source code and latest release of a GitHub repository for archival purposes.

## Usage

1. **Download the script:**
   Download `ras.py` and save it to your desired location.

2. **Run the script:**
   Open a command line interface and navigate to the directory where `ras.py` is saved. Run the script using Python:
```
python ras.py
```

3. **Provide the GitHub repository URL:**
   When prompted, enter the GitHub repository URL you wish to archive.

The script will create a separate folder for each repository in the directory where the script is located. The folder name will include the repository name and the current date.

## Features

- **Automatic Source Code Download:** Fetches the latest source code of the specified GitHub repository.
- **Release Asset Download:** Downloads the latest release assets if available.
- **Progress Bar:** Provides a visual progress bar during downloads.
- **Configurable Rate Limiting:** Includes an optional rate-limiting feature to avoid hitting GitHub API limits.

## Prerequisites

- Python 3.x
- `requests` library
- `json` library
- `zipfile` library

You can install the required libraries using:

    pip install requests

## Configuration

The script automatically generates a `config.json` file if it does not exist. This file includes a configuration setting for rate limiting:

    {
        "rate_limiting": true
    }

You can enable or disable rate limiting by setting the `rate_limiting` value to `true` or `false`.

## Example

     python ras.py

Example prompt and input:

    Enter the GitHub repository URL: https://github.com/user/repo

## License

This project is licensed under the Gnu GPL 3.0 License. See the LICENSE file for details.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository.
