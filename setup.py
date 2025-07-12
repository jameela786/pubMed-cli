"""
Setup script for pubmed-pharma-papers package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="get-papers-list",
    version="0.1.0",
    author="User",
    author_email="user@example.com",
    description="Python program to fetch research papers from PubMed API and identify pharmaceutical/biotech company affiliations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "get-papers-list=pubmed_pharma_papers.cli:main",
        ],
    },
    keywords="pubmed, pharmaceutical, biotech, research papers, bioinformatics",
    project_urls={
        "Bug Reports": "https://github.com/user/pubmed-pharma-papers/issues",
        "Source": "https://github.com/user/pubmed-pharma-papers",
    },
) 