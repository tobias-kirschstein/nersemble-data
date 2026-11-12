from pathlib import Path

from environs import Env

from nersemble_data.constants import SUBSET_URL_SUFFIXES

env = Env(expand_vars=True)
env_file_path = Path(f"{Path.home()}/.config/nersemble_data/.env")
if env_file_path.exists():
    env.read_env(str(env_file_path), recurse=False)

with env.prefixed("NERSEMBLE_"):
    NERSEMBLE_DATA_URL = env("DATA_URL", f"<<<Define NERSEMBLE_DATA_URL in {env_file_path}>>>")

REPO_ROOT = f"{Path(__file__).parent.resolve()}/../.."


def get_data_url(subset: str = 'main') -> str:
    """
    Base URL of the specified NeRSemble subset.
    All subsets live next to the main dataset, e.g., <NERSEMBLE_DATA_URL>-hair for the hair subset.
    The URL is looked up at call time, so that a URL entered at the prompt is picked up as well.
    """

    assert subset in SUBSET_URL_SUFFIXES, f"Unknown subset {subset}. Available subsets: {list(SUBSET_URL_SUFFIXES.keys())}"
    base_url = NERSEMBLE_DATA_URL.rstrip('/')
    return f"{base_url}{SUBSET_URL_SUFFIXES[subset]}"
