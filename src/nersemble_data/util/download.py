import os
import urllib
from pathlib import Path
from urllib.error import HTTPError, URLError

import requests
from elias.util import ensure_directory_exists_for_file


def download_file(url: str, target_path: str) -> None:
    ensure_directory_exists_for_file(target_path)

    if Path(target_path).exists():
        response = requests.head(url)
        download_size = int(response.headers['content-length'])
        local_file_size = os.path.getsize(target_path)

        if download_size == local_file_size:
            print(f"{target_path} already exists, skipping")
            return
        else:
            print(f"{target_path} seems to be incomplete. Re-downloading...")

    print(f"Downloading file from {url} to {target_path}")

    try:
        urllib.request.urlretrieve(url, target_path)
    except HTTPError as e:
        print(f"HTTP error occurred reaching {url}: {e}")
    except URLError as e:
        print(f"URL error occurred reaching {url}: {e}")
