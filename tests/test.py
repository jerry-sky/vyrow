#!/usr/bin/env python3

from typing import List
from os import system as _execute, path as os_path, listdir as ls
from utilities import parent_path, current_path
import suite

pjoin = os_path.join


def execute(*args: List[str]) -> None:
    _execute(r' '.join(args))


# get all the paths of the necessary files
pandoc_script_path = pjoin(parent_path(), 'pandoc.sh')
template_head = pjoin(parent_path(), 'template', 'head.html')
template_pandoc = pjoin(parent_path(), 'template', 'pandoc-template.html')
template_style = pjoin(parent_path(), 'template', 'style.css')


for doc in ls(pjoin(current_path(), 'documents')):
    # go through every Markdown test document
    if doc.endswith('.md'):
        doc_name = doc
        doc = pjoin(current_path(), 'documents', doc_name)

        # run the program
        execute(
            pandoc_script_path, # run the pandoc script
            doc, # on this test document file
            template_pandoc, template_style, template_head, # with default template files
            '>', doc.replace('.md', '.html') # and save the output to an HTML file
        )

        # execute the test suite for this particular file
        getattr(suite, doc_name.replace('.md', ''))()
