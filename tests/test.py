#!/usr/bin/env python3

from typing import List, Tuple
from types import FunctionType
from os import system as _execute, path as os_path, listdir as ls
from utilities import parent_path, current_path
import suite
from inspect import getmembers, isfunction

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

# get all tests in the test suite
# format: (function, function doc)
tests: List[Tuple[FunctionType, str]] = filter(
    # filter out those that do not contain references to Markdown documents
    lambda fff: fff[1].endswith('.md'),
    [
        # get all functions with their docs
        (ff[1], ff[1].__doc__.strip()) if ff[1].__doc__ is not None else (None, '') for ff in filter(
            lambda f: isfunction(f[1]),
            getmembers(suite)
        )
    ]
)

for t in tests:
    test = t[0]
    doc = t[1]
    # execute test
    print(doc, 'initialised')
    test()
    print(doc, 'ran successfully')
