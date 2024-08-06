# RepositoryArchiveScript *(aka RAS)*

A Python script designed to easily allow you to download the source code and latest release of a GitHub repository for archival purposes.

I made this script for my personal use but decided to upload it here as it may also be useful to others who have similar needs.
I had fun making the repo look all official :P

## Usage
1. **[Download and install Python](https://wiki.python.org/moin/BeginnersGuide/Download)** 

2. **Install requirements:** Open a command line interface and install the `requests` package using pip:
```
pip install requests
```
3. **Download the script:**
   Download `ras.py` ~~_(sounds like raspi, funny!!)_~~ and save it to your desired location.

4. **Run the script:**
   Open a command line interface and navigate to the directory where `ras.py` is located. Run the script using Python, ex:
```
python ras.py
```
5. **Accept the terms:**
   Type 'yes' or 'no' to accept/deny the terms ***(you will only have to do this once)***

6. **Provide the GitHub repository URL:**
   When prompted, enter the GitHub repository URL you wish to download.

The script will create a separate folder for each repository in the directory where the script is located. The folder name will include the repository name and the current date.

## Features

- **Automatic Source Code Download:** Fetches the latest source code of the specified GitHub repository.
- **Release Asset Download:** Downloads the latest release assets if available.
- **Progress Bar:** Provides a visual progress bar during downloads.
- **Configurable Rate Limiting:** Includes an optional rate-limiting feature to avoid hitting GitHub API limits.

## Prerequisites

- Python 3.x
- `requests` library

You can install the required libraries using:

    pip install requests

## Configuration

The script automatically generates a `config.json` file if it does not exist. This file includes a configuration setting for rate limiting:

    {
        "rate_limiting": true
        "terms_confirmed": false
    }

You can enable or disable rate limiting by setting the `rate_limiting` value to `true` or `false`.

`terms_confirmed` is set to true when the user accepts the terms.

## License & disclaimer
This project is licensed under the GNU General Public License v3.0 (GPL-3.0). This software is provided "as is," without any express or implied warranties. I make no guarantees regarding the functionality, reliability, or suitability of this software for any particular purpose.

By using this software, you acknowledge that it may not work as intended or may have defects or issues. I am not liable for any damages or problems that arise from the use of this software.

If you encounter any issues or bugs, please feel free to report them, but understand that I may not be able to address them.

### Terms of Service

When using this software, you are required to adhere to GitHub's Terms of Service, Terms of Use, and other terms. Ensure that your use of this script complies with these terms.

### Download and Use at Your Own Risk

This script automatically downloads a GitHub repository, but it is your responsibility to verify the safety of any content downloaded using this script. Ensure that the repositories or files you are downloading and the URLs you input are from trusted sources. I am not responsible for the content of any files downloaded through this script or for any damages or issues that may arise from their use.

For more details on the GNU GPL v3.0, please refer to LICENSE file.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository.
