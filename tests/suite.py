from utilities import parent_path, execute, file_tree, HTMLElement
import unittest
import os.path


PANDOC_SCRIPT_PATH = os.path.join(parent_path(), 'pandoc.sh')
# XPath prefixes
HEAD = '/html/head'
BODY = '/html/body'


class TestSuite(unittest.TestCase):
    '''
    Contains tests for some exemplary Markdown documents.
    '''

    def __execute(self, *options: list[str]):
        execute(
            PANDOC_SCRIPT_PATH,
            '--keep-original',
            '--dont-copy-stylesheet',
            '-d documents',
            *options,
        )

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
        self.__execute()
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
            'sub-header',
            'smaller-sub-header',
            'even-smaller-sub-header',
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
        self.__execute()
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
        self.__execute()
        tree = file_tree('Document only with a H1 header.html')

        self.assertRegex(tree.xpath(f'{HEAD}/title/text()')[0], r'Document\stitle\sin\sa\sheader H1')

        self.assertRegex(tree.xpath(f'{BODY}/p[1]/text()')[0], r'content')

    def test_toc_h1_header(self):
        '''
        Document with a H1 header as title and sections to verify a valid ToC is generated.
        '''
        self.__execute('--toc')
        tree = file_tree('toc/ToC with a H1 header.html')

        document_header_element: HTMLElement = tree.xpath(f'{BODY}/*[1]')[0]
        self.assertEqual(document_header_element.tag, 'h1')
        self.assertEqual(document_header_element.text, 'Document')

        toc_element: HTMLElement = tree.xpath(f'{BODY}/*[2]')[0]
        self.assertEqual(toc_element.tag, 'nav')
        self.assertEqual(toc_element.attrib['id'], 'TOC')

        list_element = 'ul[1]/li[1]/'

        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[1]/a/text()')[0], r'Section')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[1]/{list_element * 1}a/text()')[0], r'Sub-section')

        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/a/text()')[0], r'Another\ssection')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}a/text()')[0], r'Another\ssub-section')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 2}a/text()')[0], r'Deeper\ssection')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 3}a/text()')[0], r'Level\sfive\ssection')
        # level six section should not be displayed in the ToC
        self.assertEqual(len(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 4}a')), 0)

    def test_toc_number_sections(self):
        '''
        Document to verify a valid ToC is generated with numbered sections.
        '''
        self.__execute('--toc', '--number-sections')
        tree = file_tree('toc/ToC.html')

        header_element: HTMLElement = tree.xpath(f'{BODY}/*[1]')[0]
        self.assertEqual(header_element.tag, 'header')
        self.assertEqual(header_element.attrib['id'], 'title-block-header')

        description_element: HTMLElement = tree.xpath(f'{BODY}/*[2]')[0]
        self.assertEqual(description_element.tag, 'p')
        self.assertEqual(description_element.attrib['id'], 'document-description')

        toc_element: HTMLElement = tree.xpath(f'{BODY}/*[3]')[0]
        self.assertEqual(toc_element.tag, 'nav')
        self.assertEqual(toc_element.attrib['id'], 'TOC')

        list_element = 'ul[1]/li[1]/'

        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[1]/a/span[@class="toc-section-number"]/text()')[0], r'1\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[1]/a/text()')[0], r'\sSection')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[1]/{list_element * 1}a/span[@class="toc-section-number"]/text()')[0], r'1\.1\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[1]/{list_element * 1}a/text()')[0], r'\sSub-section')

        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/a/span[@class="toc-section-number"]/text()')[0], r'2\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/a/text()')[0], r'\sAnother\ssection')

        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}a/span[@class="toc-section-number"]/text()')[0], r'2\.1\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}a/text()')[0], r'\sThree')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 2}a/span[@class="toc-section-number"]/text()')[0], r'2\.1\.1\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 2}a/text()')[0], r'\sFour')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}/ul[1]/li[2]/a/span[@class="toc-section-number"]/text()')[0], r'2\.1\.2\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}/ul[1]/li[2]/a/text()')[0], r'\sFour\s2nd')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}/ul[1]/li[2]/{list_element * 1}a/span[@class="toc-section-number"]/text()')[0], r'2\.1\.2\.1\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/{list_element * 1}/ul[1]/li[2]/{list_element * 1}a/text()')[0], r'\sFive')

        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/ul[1]/li[2]/a/span[@class="toc-section-number"]/text()')[0], r'2\.2\.')
        self.assertRegex(tree.xpath(f'{BODY}/nav[1]/ul[1]/li[2]/ul[1]/li[2]/a/text()')[0], r'\sThree 2nd')
