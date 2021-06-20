from lxml import html as HTML
from utilities import file_contents, current_path
from os import path as os_path
import unittest


HTMLElement = HTML.HtmlElement


def file_tree(filename: str):
    return HTML.fromstring(file_contents(os_path.join(current_path(), 'documents', filename)))


# XPath prefixes
HEAD = '/html/head'
BODY = '/html/body'


class TestSuite(unittest.TestCase):
    '''
    Contains tests for some exemplary Markdown documents.
    '''

    def main(self):
        unittest.main()

    def __one_h1_element(self, tree: HTMLElement) -> HTMLElement:
        '''
        Asserts there is only one `h1` tag in the document
        and returns it.
        '''
        main_header = tree.xpath(f'{BODY}/*/h1')
        self.assertEqual(len(main_header), 1)
        return main_header[0]

    def test_simple(self):
        '''
        simple.md
        '''
        tree = file_tree('simple.html')

        document_title = 'Simple example document'

        # check the document title
        self.assertEqual(tree.xpath(f'{HEAD}/title/text()')[0], document_title)

        # check if the document contains only one header
        main_header = self.__one_h1_element(tree)

        # check the header contents
        self.assertEqual(main_header.text_content(), document_title)

        # check the first paragraph
        self.assertEqual(
            tree.xpath(f'{BODY}/p/em/text()')[0],
            'A simple test document.'
        )

        # check the ids of the headers
        self.assertEqual(tree.xpath(f'{BODY}//@id'), [
            'title-block-header',
            '1-sub-header',
            '11-smaller-sub-header',
            '111-even-smaller-sub-header',
        ])

        # partially check for the KaTeX maths
        self.assertEqual(
            tree.xpath(f'{BODY}/p[2]//annotation/text()')[0],
            '\n\\sum_{k=0}^n = 2^n.\n'
        )
        # check if parts of the math expression are present
        math_spans = tree.xpath(
            f'{BODY}/p[2]//span[@class="katex-html"][1]//span/text()')
        self.assertIn('k', math_spans)
        self.assertIn('n', math_spans)
        self.assertIn('=', math_spans)
        self.assertIn('0', math_spans)
        self.assertIn('∑', math_spans)

        # check the list
        unordered_list = tree.xpath(f'{BODY}/ul')
        # assert that there is such list
        self.assertEqual(len(unordered_list), 1)
        # assert that the list contains three elements
        ul_items = tree.xpath(f'{BODY}/ul/li')
        self.assertEqual(len(ul_items), 3)

        # same test with the ordered list
        ordered_list = tree.xpath(f'{BODY}/ol')
        self.assertEqual(len(ordered_list), 1)
        ol_items = tree.xpath(f'{BODY}/ol/li')
        self.assertEqual(len(ol_items), 3)

    def test_no_metadata(self):
        '''
        A document with no metadata.md
        '''
        tree = file_tree('A document with no metadata.html')

        document_title = 'A document with no metadata'

        self.assertEqual(tree.xpath(f'{HEAD}/title/text()')[0], document_title)

        self.assertEqual(tree.xpath(f'{BODY}/p[1]/text()')[0], 'content')

        self.assertEqual(
            tree.xpath(f'{BODY}/p[2]/em/text()')[0],
            'some more content'
        )

        self.assertEqual(
            tree.xpath(
                f'{BODY}/p[3]/span[@class = "katex"]//semantics//mtext//text()')[0],
            'LaTeX'
        )

        self.assertEqual(
            tree.xpath(
                f'{BODY}/p[3]/span[@class = "katex"]//span[@class = "katex-html"]//text()'),
            list('LATE\u200bX')
        )

    def test_h1_header_title(self):
        '''
        Document only with a H1 header.md
        '''
        tree = file_tree('Document only with a H1 header.html')

        document_title = 'Document title in a header H1'

        self.assertEqual(tree.xpath(f'{HEAD}/title/text()')[0], document_title)

        self.assertEqual(tree.xpath(f'{BODY}/p[1]/text()')[0], 'content')
