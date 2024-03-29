from sys import argv
from lxml import html as HTML
import os

HTMLElement = HTML.HtmlElement


def file_contents(path: str) -> str:
    '''
    Returns contents of a given file.
    '''
    with open(path, 'r+') as f:
        return f.read()


def current_path() -> str:
    '''
    Returns the path to the current script running directory.
    '''
    return os.path.dirname(argv[0]) or '.'


def parent_path() -> str:
    '''
    Returns the path to the parent directory of the current script running directory.
    '''
    # get the directory that contains the running script
    cwd = current_path()

    # calculate the parent directory
    pp = ''
    if cwd == '.':
        # the directory running is the `tests` directory
        pp = '..'
    else:
        # otherwise go one directory level up
        pp = os.path.dirname(cwd)

    if pp == '':
        # the script has been initiated from the repository directory
        pp = '.'

    return pp


def execute(*args: list[str]) -> None:
    os.system(r' '.join(args))


def file_tree(filename: str) -> HTMLElement:
    return HTML.fromstring(file_contents(os.path.join(current_path(), 'documents', filename)))
