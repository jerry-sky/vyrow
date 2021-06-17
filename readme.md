# VYROW — View Your Repository On the Web

*This GH Action takes all Markdown documents from a given repository and renders them into HTML documents. The output may be used as web representation of the repository.*

---

- [1. Motivation](#1-motivation)
- [2. How does it work](#2-how-does-it-work)
- [3. How to use](#3-how-to-use)
    - [3.1. Parameters](#31-parameters)
        - [3.1.1. `source-directory`](#311-source-directory)
        - [3.1.2. `pandoc-script`](#312-pandoc-script)
        - [3.1.3. `pandoc-template`](#313-pandoc-template)
        - [3.1.4. `stylesheet`](#314-stylesheet)
        - [3.1.5. `stylesheet-base-href`](#315-stylesheet-base-href)
        - [3.1.6. `head`](#316-head)
        - [3.1.7. `copy-master`](#317-copy-master)
    - [3.2. General use-case](#32-general-use-case)
- [4. Some remarks](#4-some-remarks)
- [5. Changes in version `0.6.0`](#5-changes-in-version-060)
- [6. Licence](#6-licence)

---

## 1. Motivation

Some repositories rely heavily on text-based content, meaning they have very little source code but a lot of human-readable documents.

Examples of such repositories are my repository notebooks:

- [`personal-notebook`](https://personal.jerry-sky.me)
- [`academic-notebook`](https://academic.jerry-sky.me)

Of course, it does not matter what is the ratio of source files to document files — this little tool is useful when it comes to creating websites from Markdown documents already present in the repository.

---

## 2. How does it work

This GH Action copies the whole input repository to the `dist` directory and then uses [Pandoc](https://pandoc.org/) for rendering all Markdown documents contained in that repository.

The main `readme.md` file (in the root of the repository) is treated as the landing page of the repository thus it is renamed to `index.html`.

By default, LaTeX expressions are rendered using the [Pandoc-KaTeX](https://github.com/xu-cheng/pandoc-katex) Rust package.\
You can change that behaviour by providing your own script that calls Pandoc differently.

---

## 3. How to use

Use it as an GH Action in your workflow:

```yml
name: 'render the repository as a website'
uses: 'jerry-sky/vyrow@v0.5.4'
```

The action will create (if it does not already exist) a directory called `dist` inside the provided `source-directory` with HTML documents created from Markdown documents.

### 3.1. Parameters

All parameters are optional as all of them have their own default values.\
However, it is encouraged to at least review what options are available that allow customization of this GH Action.

#### 3.1.1. `source-directory`

Default value: `.`

The source directory that contains all Markdown documents (and other files) that need to be converted into HTML documents.

#### 3.1.2. `pandoc-script`

Default value: [the default script contained in this repository](pandoc.sh)

The Bash script that runs `pandoc` to convert every single `.md` file into `.html` file.

If you want to customize this parameter, you can point it to a Bash script that runs `pandoc` with options provided by you.\
Please mind the order of the arguments provided for the script:
1. the file to convert
2. the pandoc HTML template
3. the stylesheet file
4. additional code to insert into `<head>` in the output document

#### 3.1.3. `pandoc-template`

Default value: [template contained in this repository](template/pandoc-template.html)

The HTML template to use when conversion from Markdown to HTML occurs.

Please refer to the [*Pandoc Manual*](https://pandoc.org/MANUAL.html#templates) for additional details.

#### 3.1.4. `stylesheet`

Default value: [template contained in this repository](template/style.css)

CSS stylesheet that is used for displaying output documents.

#### 3.1.5. `stylesheet-base-href`

Default value: `/`

This is the value that would be used in the `<base href="?">` tag in the `<head>` of the HTML output document. However, because the rendered Markdown documents may contain relative links between them and adding e.g. `<base href="/">` would break it.\
Thus, we want to apply this behaviour *only* to this stylesheet.

This is useful if the website is anchored not on the root of the domain. For example, you could have the root URL of the website like `https://username.github.io/repository/`, so the `stylesheet-base-href` parameter should be set to `/repository/`.

#### 3.1.6. `head`

Default value: [template contained in this repository](template/head.html)

Contents of the provided file will be directly inserted into the `<head>` element of the output document.

---

#### 3.1.7. `copy-master`

Default value: `'false'`

Copy all files in the master branch to the `dist` directory first. Turned off by default.

*To turn on this feature please provide a string, namely `'true'`, not a boolean value.*

---

### 3.2. General use-case

Here is an example for how to use this GH Action that will meet needs of most people.

```yml
# This workflow renders all Markdown documents into a HTML website.

name: 'Build the website'

on:
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
        uses: 'jerry-sky/vyrow@v0.6.0'
        with:
          # copy all files in the master branch to the `dist` directory
          # to make all files visible to the public
          # you can turn off this feature and cherry-pick yourself
          # only those files that you need to publish
          copy-master: 'true'

      # get current time to mark it in the deployment commit message
      - name: 'Get current time'
        uses: gerred/actions/current-time@master
        id: current-time

      # deploy the result to the GH Pages
      - name: push the changes
        uses: EndBug/add-and-commit@v7.2.1
        with:
          message: "deployed on ${{ steps.current-time.outputs.time }}"
          branch: 'gh-pages'
          cwd: './dist/'
          add: '*'
          default_author: github_actions

```

1. First, we check out the repository — the main branch to the current directory and the `gh-pages` one to the `dist` directory.
2. Then we use this GH Action to render out the documents.
3. Finally, we commit these changes to the `gh-pages` branch.

This use-case assumes you have `gh-pages` branch already created and GH Pages feature turned on in the settings in your repository.

---

## 4. Some remarks

One can say that this is a glorified GitHub’s Wiki feature. However, I would argue that this way of handling Docs, Wikis or anything of that sort is just another way which gives more flexibility. This GH Action may be only one tool of many present in one’s website pipeline.

---

## 5. Changes in version `0.6.0`

In version `0.6.0` VYROW will **not** copy all files from the master branch
to the `dist` directory automatically by default.
This feature is now **disabled** by default.

To enable it please see the [`copy-master`](#317-copy-master) parameter section.

---

## 6. Licence

See [LICENSE.md](LICENSE.md) for details about licencing of this GH Action.

---
