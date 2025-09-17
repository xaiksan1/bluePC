#!/usr/bin/env python3
"""
Setup script for Gemini AI Connector
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gemini-ai-connector",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive tool to connect and interact with Google's Gemini AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gemini-ai-connector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gemini-connector=src.gemini_connector:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.json", "config/*.template"],
    },
)