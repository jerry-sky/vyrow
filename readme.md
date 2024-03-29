# VYROW — View Your Repository On the Web

*This GH Action takes all Markdown documents from a given repository*
*and renders them into HTML documents.*
*The output may be used as a web representation of the repository.*

---

- [1. Motivation](#1-motivation)
- [2. How does it work](#2-how-does-it-work)
    - [2.1. In general](#21-in-general)
    - [2.2. Specifics](#22-specifics)
        - [2.2.1. Markdown format](#221-markdown-format)
        - [2.2.2. Table of contents (ToC)](#222-table-of-contents-toc)
        - [2.2.3. LaTeX support](#223-latex-support)
- [3. How to use](#3-how-to-use)
    - [3.1. General use-case](#31-general-use-case)
    - [3.2. Use-case for non-root websites (like `username.github.io/repository`)](#32-use-case-for-non-root-websites-like-usernamegithubiorepository)
- [4. Parameters](#4-parameters)
    - [4.1. `working-directory`](#41-working-directory)
    - [4.2. `pandoc-script`](#42-pandoc-script)
        - [4.2.1. Default Pandoc script](#421-default-pandoc-script)
    - [4.3. `pandoc-template`](#43-pandoc-template)
    - [4.4. `toc`](#44-toc)
    - [4.5. `number-sections`](#45-number-sections)
    - [4.6. `stylesheet`](#46-stylesheet)
    - [4.7. `website-root`](#47-website-root)
    - [4.8. `head`](#48-head)
    - [4.9. `copy-from`](#49-copy-from)
- [5. Some remarks](#5-some-remarks)
- [6. Licence](#6-licence)

---

## 1. Motivation

Some repositories rely heavily on text-based content,
meaning they have very little source code but a lot of human-readable documents.

Examples of such repositories are my repository notebooks:

- [`personal-notebook`](https://personal.jerry-sky.me)
- [`academic-notebook`](https://academic.jerry-sky.me)

Of course, it does not matter what is the ratio of source files to document files
— this little tool is useful when it comes to creating websites
from Markdown documents already present in the repository.

---

## 2. How does it work

### 2.1. In general

This GH Action uses [Pandoc](https://pandoc.org) to render Markdown documents
into HTML documents to then be published to e.g. Github Pages.

The main `readme.md` file (in the root of the repository) is treated as
the landing page of the repository, and thus it is renamed to `index.html`.

### 2.2. Specifics

#### 2.2.1. Markdown format

The [default Pandoc script](pandoc.sh) converts from `markdown` to `html`
with following [Pandoc extensions](https://pandoc.org/MANUAL.html#extensions):

- *disabled* `blank_before_header`,
- *disabled* `implicit_figures`,
- *enabled* `lists_without_preceding_blankline`,
- *enabled* `gfm_auto_identifiers`,

thus, the Pandoc `--from` option is set to
`markdown-blank_before_header-implicit_figures+lists_without_preceding_blankline+gfm_auto_identifiers`.

*This format is pretty close to the GitHub-flavoured Markdown.*

The Pandoc built-in `gfm` format that simulates mentioned flavour was not used,
because it does not allow for LaTeX expressions.

Please refer to the [Pandoc manual](https://pandoc.org/MANUAL.html)
for further details regarding the program itself.

#### 2.2.2. Table of contents (ToC)

A table of contents will be generated based on document’s headers of level 2 and higher.

Example:\
Given document of contents:
```md
# Document

## Section one

Contents.

## Section two

### Sub-section

Contents.

## Section three

Contents.
```

will result in an output of:

![Example document with an generated ToC (a screenshot of a rendered HTML document)](toc_example_document.png)

ToC will be inserted after the first level one header (`h1` in HTML, `# ` in Markdown),
or after the contents generated from the
[YAML metadata block](https://pandoc.org/MANUAL.html#extension-yaml_metadata_block)
if it’s present in the document.

#### 2.2.3. LaTeX support

As [mentioned above](#221-markdown-format) the Markdown format we’re using
allows for LaTeX expressions to be added to the rendered documents.

By default, LaTeX expressions are rendered using the
[Pandoc-KaTeX](https://github.com/xu-cheng/pandoc-katex) Rust package.\
You can change this behaviour by
[providing your own script](#42-pandoc-script) that calls Pandoc differently.

---

## 3. How to use

Use it as a part of your GH Actions workflow:

```yml
name: 'render the repository as a website'
uses: 'jerry-sky/vyrow@v0.8.0'
```

The action will create (if it does not already exist) a directory called `dist`
where you can put your Markdown documents to convert and other files,
that will be simply ignored.

It is advised you should look at use-cases listed below,
before implementing it yourself, to better understand how does it work.

### 3.1. General use-case

Here is an example for how to use this GH Action that will meet
needs of most people that want to publish a website on a root domain,
say `website.com`.

```yml
# This workflow renders all Markdown documents into a HTML website.

name: 'Build the website'

on:
  # re-render the website every time new changes are pushed
  push:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # checkout the `master` branch
      - name: 'Checkout `master`'
        uses: actions/checkout@v2.3.4

      # prepare the `gh-pages` branch to publish the repository as a website
      - name: 'Checkout `gh-pages` into a separate directory'
        uses: actions/checkout@v2.3.4
        with:
          path: 'dist'
          ref: 'gh-pages'

      # use this action to render all Markdown documents into HTML documents
      - name: 'Render the repository as a website'
        uses: 'jerry-sky/vyrow@v0.8.0'
        with:
          # copy all files from the master branch to the `dist` directory
          # to make all files visible on the website;
          # this option is turned off by default,
          # so you can cherry-pick yourself only those files
          # that you want to publish
          copy-from: '.'

      # get current time to mark it in the deployment commit message
      - name: 'Get current time'
        uses: gerred/current-time@v1.0.0
        id: current-time

      # deploy the result to the GH Pages branch
      - name: push the changes
        uses: EndBug/add-and-commit@v7.2.1
        with:
          message: "deployed on ${{ steps.current-time.outputs.time }}"
          branch: 'gh-pages'
          cwd: './dist/'
          add: '*'
          default_author: github_actions

```

1. First, we check out the repository
    — the main branch to the current directory and the `gh-pages` one
    to the `dist` directory.
2. Then we use VYROW to render out the documents.
3. Finally, we commit these changes to the `gh-pages` branch.

This use-case assumes you have `gh-pages` branch already created
and GH Pages feature turned on in the settings in your repository.

### 3.2. Use-case for non-root websites (like `username.github.io/repository`)

When dealing with a website that will not be anchored at the root of the domain,
you need to specify the website root.

For example, you have a repository on GitHub you want to publish.
The GH Pages website address will be something like
`username.github.io/repository`.
Then, you have to specify the `website-root` option

```yml
website-root: '/site/'
```

when calling VYROW in your build workflow.

After applying that to the [general use-case](#31-general-use-case)
you will have:

```yml
- name: 'Render the repository as a website'
  uses: 'jerry-sky/vyrow@v0.8.0'
  with:
    copy-from: '.'
    website-root: '/repository/'
```

in the VYROW section of your workflow.

---

## 4. Parameters

All parameters of this GH Action are optional.\
However, it is encouraged to at least review what options are available
that allow customization of this GH Action.

---

### 4.1. `working-directory`

*The directory containing the source Markdown documents that will be*
*converted into output HTML documents.*

Default value: `dist`

You can also attach other files you want to publish alongside the website.

---

### 4.2. `pandoc-script`

*The Bash script that runs Pandoc to convert Markdown documents into HTML documents.*

If not provided the [default script contained in this repository](pandoc.sh) will be used.

If you want to customize this parameter, you can point it to
a Bash script that runs `pandoc` with options provided by you.
Please note that your custom script must comply with the switches
list of the default Pandoc script.

#### 4.2.1. Default Pandoc script

The default script accepts following options (switches):

- `-t` — custom [Pandoc HTML5 template](#43-pandoc-template),
- `-s` — custom [CSS stylesheet](#44-stylesheet),
- `-h` — custom [headers file containing additional tags to include in the `<head>` of all output HTML documents](#46-head),
- `-d` — the [working directory](#41-working-directory),
- `-r` — the [root of the website](#45-website-root).

All options require values to be given.\
The `-d` option is required.

---

### 4.3. `pandoc-template`

*The HTML template to use when converting Markdown documents to HTML documents.*

If not provided, the [template contained in this repository](template/pandoc-template.html) will be used.

Please refer to the [*Pandoc Manual*](https://pandoc.org/MANUAL.html#templates) for additional details.

---

### 4.4. `toc`

*Generate a ToC based on document’s level 2+ headings.*

Turned on by default.\
Set this to `0` to disable this feature.

---

### 4.5. `number-sections`

*Add numbering to section headers.*

Turned off by default.\
Set this to `1` to enable this feature.

---

### 4.6. `stylesheet`

*CSS stylesheet that is used for displaying output documents.*

If not provided, the [template contained in this repository](template/style.css)
will be used.

---

### 4.7. `website-root`

*This is the value that would be used in the `<base href="|>here<|">`*
*tag in the `<head>` of the HTML output document.*

However, because the rendered Markdown documents may contain relative
links between them and adding e.g. `<base href="/">` would break it.\
Thus, we want to apply this behaviour *only* to global files like
the stylesheet file.

This option should be used if the website is not anchored on the root
of the domain.
For example, you could have the root URL of the website like
`https://username.github.io/repository/`,
so the `website-root` parameter should be set to `/repository/`.

If not provided, then `/` will be used.

---

### 4.8. `head`

*Contents of the provided file will be directly inserted into the*
*`<head>` element of all output HTML documents.*

If not provided,
the [template contained in this repository](template/head.html) will be used.

---

### 4.9. `copy-from`

*Copy all files from given directory to the [working directory](#41-working-directory).*

Turned off by default.

This option may be handy in a use-case where you want to publish
the whole repository.
In that case you can set this option to a value of `'.'` to copy all
files from the checked out `master` branch to the
[working directory](#41-working-directory).

---

## 5. Some remarks

One can say that this is a glorified GitHub’s Wiki feature.
However, I would argue that this way of handling Docs, Wikis, notes
or anything of that sort is just another way of doing it,
which gives more options, flexibility.
This GH Action may be just one tool of many present in one’s website building pipeline.

---

## 6. Licence

See [LICENSE.md](LICENSE.md) for details about licencing of this GH Action.

---
