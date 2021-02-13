import base64
import getpass
import os
import subprocess
import sys
from pathlib import Path


def get_pypirc(art_url: str, user: str, password: str) -> str:
    return f"""
[distutils]
index-servers = local
[local]
repository: https://{art_url}/pypi/pypi
username: {user}
password: {password}
"""


def get_npmrc(art_url: str, user: str, password: str, email: str) -> str:
    user_pass = f"{user}:{password}"
    b64_user_pass = base64.b64encode(user_pass.encode("ascii")).decode("ascii")
    return f"""
registry=https://{art_url}/npm/npm/
_auth = {b64_user_pass}
email = {email}
always-auth = true
"""


def configure_pip(art_url: str, user: str, password: str) -> None:
    index_url = f"https://{user}:{password}@{art_url}/pypi/pypi/simple"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "config",
            "set",
            "global.index",
            index_url,
        ]
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "config",
            "set",
            "global.index-url",
            index_url,
        ]
    )


def save_file(path: Path, contents: str) -> None:
    if path.is_file():
        print(f"{path} found, not writing")
        return

    if not path.parent.is_dir():
        os.makedirs(str(path.parent))

    with path.open("w") as fp:
        fp.write(contents)


def main() -> None:
    art_url = sys.argv[1] if len(sys.argv) > 1 else None
    user = sys.argv[2] if len(sys.argv) > 2 else None
    email = sys.argv[3] if len(sys.argv) > 3 else None
    api_key = sys.argv[4] if len(sys.argv) > 4 else None

    if not art_url:
        art_url = input("Enter your Artifactory URL: ")

    if not user:
        user = input("Enter your Artifactory User Profile: ")

    if not email:
        email = input("Enter your Artifactory Email Address: ")

    if not api_key:
        api_key = getpass.getpass(prompt="Enter your Artifactory API Key: ")

    save_file(Path.home().joinpath(".pypirc"), get_pypirc(art_url, user, api_key))
    save_file(Path.home().joinpath(".npmrc"), get_npmrc(art_url, user, api_key, email))
    configure_pip(art_url, user, api_key)


if __name__ == "__main__":  # pragma: no cover
    main()
