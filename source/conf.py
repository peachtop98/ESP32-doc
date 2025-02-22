# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ESP32'
copyright = '2025, xavier-'
author = 'xavier-'
release = '1.8'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # 自动生成文档
    'sphinx.ext.viewcode',  # 显示源代码
    'myst_parser',  # 支持 Markdown 文件
]

# 设置源文件后缀，支持 Markdown
source_suffix = {
#    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

language = 'zh'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'   classic
html_theme = 'sphinx_rtd_theme' #切换主题
html_static_path = ['_static']

#autodoc_mock_imports 会阻止Sphinx实际导入指定模块
# 添加以下配置
autodoc_mock_imports = [
    'machine', 'time', 'utime', 'uos', 
    'framebuf', 'neopixel', 'micropython',
    'Pin', 'PWM', 'ADC', 'I2C', 'SPI',
    'SSD1306_I2C',  # 添加缺失的逗号
    'const', 'AHT20', 'QMI8658', 'ssd1306',
    'onewire', 'ds18x20', 'mfrc522_i2c'
]


#----------------------------------------------------------------------------------#
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sphinxcontrib")

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('../src/include'))