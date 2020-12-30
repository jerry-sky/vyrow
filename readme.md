---
lang: 'en-GB'
pagetitle: 'VYROW — View Your Repository On the Web'
author: 'Jerry Sky'
description: 'This GH Action takes all Markdown documents from a given repository and renders them into HTML documents. The output may be used as web representation of the repository.'
keywords: 'vyrow, view, web, html, markdown, repository, gh actions, github, actions, render, convert, document, pandoc, website'
---

# VYROW — View Your Repository On the Web

*This GH Action takes all Markdown documents from a given repository and renders them into HTML documents. The output may be used as web representation of the repository.*

---

- [1. Motivation](#1-motivation)
- [2. How to use](#2-how-to-use)
    - [2.1. Parameters](#21-parameters)
        - [2.1.1. `source-directory`](#211-source-directory)
        - [2.1.2. `pandoc-script`](#212-pandoc-script)
        - [2.1.3. `pandoc-template`](#213-pandoc-template)
        - [2.1.4. `stylesheet`](#214-stylesheet)
        - [2.1.5. `stylesheet-base-href`](#215-stylesheet-base-href)
        - [2.1.6. `head`](#216-head)
    - [2.2. General use-case](#22-general-use-case)
- [3. Some remarks](#3-some-remarks)

---

## 1. Motivation

Some repositories rely heavily on text-based content, meaning they have very little source code but a lot of human-readable documents.

Examples of such repositories are my repository notebooks: e.g. my [`personal-notebook`](https://personal-notebook.jerry-sky.me) where almost all the files are Markdown documents and there are no source files that are compilable or runnable apart from the `config` directory where I keep my settings, setup scripts and such.

Of course, it does not matter what is the ratio of source files to document files — this little tool is useful when it comes to creating websites from Markdown documents already present in the repository.

---

## 2. How to use

Use it as an GH Action in your workflow:
```yml
name: 'render the repository as a website'
uses: 'jerry-sky/vyrow@v1.0'
```

The action will create (if it does not already exist) a directory called `dist` inside the provided `source-directory` with HTML documents created from Markdown documents.

### 2.1. Parameters

All parameters are optional as all of them have their own default values.\
However, it is encouraged to at least review what options are available that allow customization of this GH Action.

#### 2.1.1. `source-directory`

Default value: `.`

The source directory that contains all Markdown documents (and other files) that need to be converted into HTML documents.

#### 2.1.2. `pandoc-script`

Default value: [the default script contained in this repository](pandoc.sh)

The Bash script that runs `pandoc` to convert every single `.md` file into `.html` file.

If you want to customize this parameter, you can point it to a Bash script that runs `pandoc` with options provided by you.\
Please mind the order of the arguments provided for the script:
1. the file to convert
2. the pandoc HTML template
3. the stylesheet file
4. additional code to insert into `<head>` in the output document

#### 2.1.3. `pandoc-template`

Default value: [template contained in this repository](template/pandoc-template.html)

The HTML template to use when conversion from Markdown to HTML occurs.

Please refer to the [*Pandoc Manual*](https://pandoc.org/MANUAL.html#templates) for additional details.

#### 2.1.4. `stylesheet`

Default value: [template contained in this repository](template/style.css)

CSS stylesheet that is used for displaying output documents.

#### 2.1.5. `stylesheet-base-href`

Default value: `/`

This is the value that would be used in the `<base href="?">` tag in the `<head>` of the HTML output document. However, because the rendered Markdown documents may contain relative links between them and adding e.g. `<base href="/">` would break it.\
Thus, we want to apply this behaviour *only* to this stylesheet.

This is useful if the website is anchored not on the root of the domain. For example, you could have the root URL of the website like `https://username.github.io/repository/`, so the `stylesheet-base-href` parameter should be set to `/repository/`.

#### 2.1.6. `head`

Default value: [template contained in this repository](template/head.html)

Contents of the provided file will be directly inserted into the `<head>` element of the output document.

---

### 2.2. General use-case

Here is an example for how to use this GH Action that will meet needs of most people.

```yml
- name: 'Checkout `master`'
  uses: actions/checkout@v2

- name: 'Checkout `gh-pages` into a separate directory'
  uses: actions/checkout@v2
  with:
    path: 'dist'
    ref: 'gh-pages'

- name: 'render the repository as a website'
  uses: 'jerry-sky/vyrow@v1.0'

- name: push the changes
  uses: EndBug/add-and-commit@v4.4.0
  with:
    message: "deployed"
    ref: 'gh-pages'
    cwd: './dist/'
    add: '*'

```

1. First, we check out the repository — the main branch to the current directory and the `gh-pages` one to the `dist` directory.
2. Then we use this GH Action to render out the documents.
3. Finally, we commit these changes to the `gh-pages` branch.

This use-case assumes you have `gh-pages` branch already created and GH Pages feature turned on in the settings in your repository.

---

## 3. Some remarks

One can say that this is a glorified GitHub’s Wiki feature. However, I would argue that this way of handling Docs, Wikis or anything of that sort is just another way which gives more flexibility. This GH Action may be only one tool of many present in one’s website pipeline.

---
