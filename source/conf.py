# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '[希科普]ESP32文档'
copyright = '2025, xavier'
author = 'xavier'
release = 'V1.8'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # 自动生成文档
    'sphinx.ext.viewcode',  # 显示源代码
    'myst_parser',  # 支持 Markdown 文件
]

# 设置源文件后缀，支持 Markdown
source_suffix = ['.md', '.rst']

templates_path = ['_templates']
exclude_patterns = []

language = 'zh'

html_search_language = 'en'  # 搜索语言设置

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'   classic   sphinx_rtd_theme    furo  press   sphinx_book_theme pydata_sphinx_theme
#好看的    press  furo
html_theme = 'furo' #切换主题
html_static_path = ['_static']

def setup(app):
    app.add_js_file('custom.js')
