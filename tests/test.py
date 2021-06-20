#!/usr/bin/env python3

from typing import List, Tuple
from types import FunctionType
from os import system as _execute, path as os_path, listdir as ls
from utilities import parent_path, current_path
from suite import TestSuite

pjoin = os_path.join


def execute(*args: List[str]) -> None:
    _execute(r' '.join(args))


pandoc_script = pjoin(parent_path(), 'pandoc.sh')

execute(
    pandoc_script,
    '--keep-original',
    '--dont-copy-stylesheet',
    '-d documents',
)

if __name__ == '__main__':
    suite = TestSuite()
    suite.main()
