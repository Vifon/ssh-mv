#!/usr/bin/env python3

from setuptools import setup

import ssh_mv

if __name__ == '__main__':
    setup(
        name='ssh-mv',
        version=ssh_mv.__version__,
        author=ssh_mv.__author__,
        license=ssh_mv.__license__,
        py_modules=['ssh_mv'],
    )
