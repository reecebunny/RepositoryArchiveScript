# RepositoryArchiveScript *(aka RAS)*

A Python script designed to easily download the source code and latest release of a GitHub repository for archival purposes.

## Usage
1. **[Download and install Python](https://wiki.python.org/moin/BeginnersGuide/Download)** 
2. **Download the script:**
   Download `ras.py` ~~_(sounds like raspi, funny!!)_~~ and save it to your desired location.

3. **Run the script:**
   Open a command line interface and navigate to the directory where `ras.py` is saved. Run the script using Python:
```
python ras.py
```

4. **Provide the GitHub repository URL:**
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

## License & disclaimer

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). This software is provided "as is," without any express or implied warranties. I make no guarantees regarding the functionality, reliability, or suitability of this software for any particular purpose.

By using this software, you acknowledge that it may not work as intended or may have defects or issues. I am not liable for any damages or problems that arise from the use of this software.

If you encounter any issues or bugs, please feel free to report them, but understand that I may not be able to address them.

### Terms of Service

When using this software, you are required to adhere to GitHub's Terms of Service and Terms of Use. Ensure that your use of this script complies with these terms.

For more details on the GNU GPL v3.0, please refer to the LICENSE file.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository.
