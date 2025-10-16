import hashlib
from pathlib import Path

from elias.util import ensure_directory_exists_for_file

from nersemble_data.constants import NERSEMBLE_ACCESS_FORM_URL
from nersemble_data.env import NERSEMBLE_DATA_URL, env, env_file_path


def _prompt_nersemble_data_url():
    print("To download the NeRSemble dataset, please do the following:")
    print(f" 1. Request access to the NeRSemble dataset via {NERSEMBLE_ACCESS_FORM_URL}")
    print(f" 2. Once your request was approved, you will receive a mail with the download url for the dataset. Enter it here")
    nersemble_data_url = input("Please enter the NERSEMBLE_DATA_URL from your access mail:")
    nersemble_data_url = nersemble_data_url.strip()

    env_dict = env.dump()
    env_dict["NERSEMBLE_DATA_URL"] = nersemble_data_url
    global NERSEMBLE_DATA_URL
    NERSEMBLE_DATA_URL = nersemble_data_url

    ensure_directory_exists_for_file(env_file_path)
    for key, value in env_dict.items():
        with open(env_file_path, "w+") as f:
            f.write(f"{key}=\"{value}\"\n")


def validate_nersemble_data_url():
    env_file_path = Path(f"{Path.home()}/.config/nersemble_data/.env")
    unset_url = f"<<<Define NERSEMBLE_DATA_URL in {env_file_path}>>>"

    if NERSEMBLE_DATA_URL == unset_url:
        _prompt_nersemble_data_url()

    while True:
        salt = "aL8jN4%Y1h%9fG7U"
        hash = hashlib.md5(f"{salt}-{NERSEMBLE_DATA_URL}".encode()).hexdigest()
        if hash == 'e6af9ecba715b6099512a125e0447c16' or hash == '39fd1782e33a6d7b41930b054e6d8aa6':
            # Correct NERSEMBLE_DATA_URL
            break
        else:
            print("The NERSEMBLE_DATA_URL that you configured is not correct.")
            _prompt_nersemble_data_url()
