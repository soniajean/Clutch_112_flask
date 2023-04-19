import os
import platform
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pathlib import Path
from getpass import getpass
from urllib.parse import urlparse
from configparser import ConfigParser
from argparse import ArgumentParser
import pkg_resources
import keyring


def main():
    """
    The main function
    """

    history = FileHistory(os.path.join(Path.home(), ".pip_login_history"))
    history.load_history_strings()

    try:
        version = pkg_resources.get_distribution(__name__).version
    except pkg_resources.DistributionNotFound:
        version = __name__ + " Unknown version"

    parser = ArgumentParser(description="pip login")
    parser.add_argument("--version", action="version", version=version)
    parser.add_argument(
        "url", nargs="?", type=str, default=None, help="The repository index URL."
    )
    parser.add_argument(
        "-u", "--username", type=str, default=None, help="The username."
    )
    parser.add_argument(
        "-p", "--password", type=str, default=None, help="The password."
    )
    parser.add_argument(
        "--plaintext",
        action="store_true",
        help="""** WARNING ** Use with caution:
            Store credentials in plain text in the pip.conf, this is useful for
            logging into a pip repository inside a docker container for CI builds.""",
    )

    args = parser.parse_args()

    url = os.environ.get("PIP_LOGIN_REPOSITORY")
    username = os.environ.get("PIP_LOGIN_USERNAME")
    password = os.environ.get("PIP_LOGIN_PASSWORD")

    if args.url:
        url = args.url
    if args.username:
        username = args.username
    if args.password:
        password = args.password

    if not url:
        url = prompt(
            "Repository URL: ", history=history, auto_suggest=AutoSuggestFromHistory()
        )
    if not username:
        username = prompt(
            "Username: ", history=history, auto_suggest=AutoSuggestFromHistory()
        )
    if not password:
        password = getpass()

    parsed_url = urlparse(url)
    netloc = parsed_url.netloc.split("@")[-1]

    if not args.plaintext:
        keyring.set_password(netloc, username, password)

    pip_conf_path = os.environ.get("VIRTUAL_ENV")
    if platform.system() == "Linux":
        if pip_conf_path:
            pip_conf_path = os.path.join(pip_conf_path, "pip.conf")
        else:
            pip_conf_path = os.path.join(Path.home(), ".config", "pip", "pip.conf")
    elif platform.system() == "Darwin":
        if pip_conf_path:
            pip_conf_path = os.path.join(pip_conf_path, "pip.conf")
        else:
            pip_conf_path = os.path.join(
                Path.home(), "Library", "Application Support", "pip", "pip.conf"
            )
    elif platform.system() == "Windows":
        if pip_conf_path:
            pip_conf_path = os.path.join(pip_conf_path, "pip.ini")
        else:
            appdata = os.environ.get("APPDATA")
            if appdata:
                pip_conf_path = os.path.join(appdata, "pip", "pip.ini")

    if args.plaintext:
        parsed_url = parsed_url._replace(netloc=f"{username}:{password}@{netloc}")
    elif not parsed_url.username:
        parsed_url = parsed_url._replace(netloc=f"{username}@{netloc}")

    extra_index_url = parsed_url.geturl()
    config = ConfigParser()

    if pip_conf_path:
        config.read(pip_conf_path)
        if "global" not in config:
            config["global"] = {}
        if "extra-index-url" not in config["global"]:
            config["global"]["extra-index-url"] = extra_index_url
        else:
            idx_url = config["global"]["extra-index-url"]
            if extra_index_url not in idx_url:
                config["global"]["extra-index-url"] = f"{idx_url}\n{extra_index_url}"
        if not os.path.exists(os.path.dirname(pip_conf_path)):
            os.makedirs(os.path.dirname(pip_conf_path))
        with open(pip_conf_path, "w+") as config_file:
            config.write(config_file)
            print(f"pip config written to: {pip_conf_path}")


if __name__ == "__main__":
    main()
