#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
  with open("README.md", "r", encoding="utf-8") as fh:
    return fh.read()

# Read requirements
def read_requirements():
  with open("requirements.txt", "r", encoding="utf-8") as fh:
    return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
  name="japanese-pdf-translator",
  version="0.1.0",
  author="Armand Li",
  author_email="armandli@example.com",
  description="Translate Japanese PDF magazines to English while retaining format",
  long_description=read_readme(),
  long_description_content_type="text/markdown",
  url="https://github.com/armandli/JapanesePDFTranslator",
  packages=find_packages(exclude=["tests*"]),
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Text Processing :: Linguistic",
    "Topic :: Multimedia :: Graphics :: Graphics Conversion",
  ],
  python_requires=">=3.8",
  install_requires=read_requirements(),
  extras_require={
    "dev": [
      "pytest>=7.0",
      "pytest-cov>=4.0",
      "black>=23.0",
      "flake8>=6.0",
      "mypy>=1.0",
    ],
  },
  entry_points={
    "console_scripts": [
      "japanese-pdf-translator=sensei.cli:main",
      "pdf-to-html=sensei.pdf_to_html:main",
    ],
  },
  include_package_data=True,
  zip_safe=False,
)
