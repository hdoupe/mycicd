import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import subprocess
import sys
import time
import tempfile
import yaml

from . import bash


__version__ = "0.0.0"


@contextmanager
def clone_repo(user_or_org, title, ref="master"):
    start = os.path.abspath(Path("."))
    cmds = []
    try:
        with tempfile.TemporaryDirectory(prefix="update-") as td:
            cmds.append(
                bash.run(f"git clone https://github.com/{user_or_org}/{title}.git {td}")
            )
            os.chdir(Path(td))

            if ref is not None:
                cmds.append(bash.run(f"git fetch origin {ref} && git checkout {ref}"))

            yield cmds
    finally:
        os.chdir(start)


def install_dependencies():
    cmds = []
    conda_env = None
    if Path("environment.yml").exists():
        cmds.append(bash.run("conda env create"))

        with open("environment.yml") as f:
            env = yaml.safe_load(f.read())
        conda_env = env["name"]

    if Path("requirements.txt").exists():
        cmds.append(bash.run("pip install -r requirements.txt", conda_env=conda_env))

    return cmds, conda_env


def run_tests(cmds, conda_env=None):
    return bash.run(cmds, batch=True, conda_env=conda_env)


def cicd(user_or_org, title, ref, test_cmd):
    with clone_repo(user_or_org, title, ref) as clone_cmds:
        install_cmds, conda_env = install_dependencies()
        if isinstance(test_cmd, str):
            test_cmd = test_cmd.split("|")
        test_cmds = run_tests(test_cmd, conda_env=conda_env)

        return clone_cmds, install_cmds, test_cmds


def handle(args):
    try:
        return cicd(args.user, args.title, args.ref, args.test_cmd)
    except bash.CommandFailed as cf:
        print("mycicd has encountered an error:")
        print(repr(cf))
        sys.exit(1)


def cli():
    parser = argparse.ArgumentParser(
        "A simple ci/cd tool. It's not secure for untrusted code but at least it's yours.\n\n"
    )
    parser.add_argument("--user", "-u", help="Username or org for git repository.")
    parser.add_argument("--title", "-t", help="Title of git repository.")
    parser.add_argument("--ref", help="Branch or commit ref to checkout.")
    parser.add_argument(
        "test_cmd", help="Command(s) to run tests. Separate commands with '|'"
    )

    parser.set_defaults(func=handle)
    args = parser.parse_args()
    args.func(args)
