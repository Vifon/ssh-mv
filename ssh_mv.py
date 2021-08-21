#!/usr/bin/env python3

__author__ = "Wojciech Siewierski"
__version__ = "1.0.0"
__license__ = "GPL3"

from os import environ
import argparse
import os.path
import shlex

import paramiko
import yaml


class InvalidFileException(Exception):
    pass


def deprefix(path, root):
    root = os.path.join(root, "")
    if path.startswith(root):
        return path[len(root):]
    else:
        raise InvalidFileException('"{}" not in "{}"'.format(path, root))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='count',
        help="Increase the verbosity level.  May be passed multiple times.",
    )
    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help="Do not actually move the files.  Makes sense only with --verbose!",
    )
    parser.add_argument('source_paths', nargs='+')
    parser.add_argument('target_path')
    args = parser.parse_args()

    config_path = os.path.join(
        environ.get(
            "XDG_CONFIG_HOME",
            os.path.join(environ["HOME"], ".config")
        ),
        "ssh-mv.yml",
    )

    with open(config_path, 'r') as fh:
        config = yaml.safe_load(fh)

    files = args.source_paths + [args.target_path]
    for n, path in enumerate(files):
        path = os.path.join(
            config["remote"]["root"],
            deprefix(
                os.path.abspath(path),
                config["local"]["root"],
            )
        )
        files[n] = path

    _ssh = None

    def ssh():
        nonlocal _ssh
        if _ssh:
            return _ssh
        else:
            _ssh = paramiko.SSHClient()
            _ssh.load_system_host_keys()
            _ssh.connect(**config["remote"]["connection"])
            return _ssh

    if args.verbose == 1:
        for x in files:
            print(x)
    elif args.verbose == 2:
        stdin, stdout, stderr = ssh().exec_command(r"printf '<%s>\n' {}".format(
            " ".join(shlex.quote(x) for x in files)
        ))
        stdout.channel.set_combine_stderr(True)
        print(stdout.read().decode(), end='')
        stdout.channel.recv_exit_status()

    if not args.dry_run:
        ssh().exec_command(r"mv -- {}".format(
            " ".join(shlex.quote(x) for x in files)
        ))
        stdout.channel.set_combine_stderr(True)
        stdout.read()
        stdout.channel.recv_exit_status()


if __name__ == '__main__':
    from sys import argv
    main(argv)
