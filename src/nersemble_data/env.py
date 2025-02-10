from pathlib import Path

from environs import Env

env = Env(expand_vars=True)
env_file_path = Path(f"{Path.home()}/.config/nersemble_data/.env")
if env_file_path.exists():
    env.read_env(str(env_file_path), recurse=False)

with env.prefixed("NERSEMBLE_"):
    NERSEMBLE_DATA_URL = env("DATA_URL", f"<<<Define NERSEMBLE_DATA_URL in {env_file_path}>>>")

REPO_ROOT = f"{Path(__file__).parent.resolve()}/../.."
