from lxml import html as HTML
from utilities import file_contents as _file_contents, current_path
from os import path as os_path
from sys import exit, stderr
from types import TracebackType
import traceback


HTMLElement = HTML.HtmlElement


def file_contents(filename: str) -> str:
    return _file_contents(os_path.join(current_path(), 'documents', filename))


# XPath prefixes
HEAD = '/html/head'
BODY = '/html/body'


# error reporting
def throw(msg: str, noexit=False) -> None:
    print('::error::\033[1mTest failed:\033[0m', msg, file=stderr)
    if not noexit:
        exit(1)


class AssertionError(BaseException):
    def __init__(self, *args, **kwargs):
        try:
            # raise an exception just to initiate the exception reporting process
            raise BaseException
        except BaseException as e:
            # ignore this fake exception
            # extract the actual assertion exception
            stack = traceback.extract_stack()
            # the assertion exception in question will be second last,
            # as the last exception in the stack is this fake exception
            # raised above
            err = stack[-2]
            # pass along what actually happened
            # pass the line where the assertion takes place
            throw('assertion failed at line ' +
                  str(err.lineno) + ': ' + err.line)


# tests to perform upon test documents of the same name
# e.g. file `simple.md` will be tested with function of name `simple`


# some staple tests performed on all test documents
def __one_h1_element(tree: HTMLElement) -> HTMLElement:

    main_header = tree.xpath(f'{BODY}/*/h1')

    if len(main_header) != 1:
        print(main_header)
        throw('number of `h1` headers are either zero or more than one')

    return main_header[0]


# tests for some exemplary Markdown documents
def simple():
    '''
    simple.md
    '''
    # get the file contents
    fc = file_contents('simple.html')
    tree = HTML.fromstring(fc)

    # check if the document contains only one header
    main_header = __one_h1_element(tree)

    # check the header contents
    assert main_header.text_content() == 'Simple example document'

    # check the first paragraph
    assert tree.xpath(f'{BODY}/p/em/text()')[0] == 'A simple test document.'

    # check the ids of the headers
    assert tree.xpath(f'{BODY}//@id') == [
        'title-block-header',
        '1-sub-header',
        '11-smaller-sub-header',
        '111-even-smaller-sub-header'
    ]

    # partially check for the KaTeX maths
    assert tree.xpath(f'{BODY}/p[2]//annotation/text()')[0] == '\n\\sum_{k=0}^n = 2^n.\n'
    # check if parts of the math expression are present
    math_spans = tree.xpath(f'{BODY}/p[2]//span[@class="katex-html"][1]//span/text()')
    assert 'k' in math_spans
    assert 'n' in math_spans
    assert '=' in math_spans
    assert '0' in math_spans
    assert '∑' in math_spans

    # check the list
    unordered_list = tree.xpath(f'{BODY}/ul')
    # assert that there is such list
    assert len(unordered_list) == 1
    # assert that the list contains three elements
    ul_items = tree.xpath(f'{BODY}/ul/li')
    assert len(ul_items) == 3

    # same test with the ordered list
    ordered_list = tree.xpath(f'{BODY}/ol')
    assert len(ordered_list) == 1
    ol_items = tree.xpath(f'{BODY}/ol/li')
    assert len(ol_items) == 3
