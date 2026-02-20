"""
Setup configuration for the Order Manager library.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="order_manager",
    version="1.0.0",
    description="Python library for managing customer orders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Team",
    author_email="team@example.com",
    url="https://github.com/yourorg/order_manager",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.25",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ]
    },
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="orders management sqlite sqlalchemy",
    project_urls={
        "Bug Reports": "https://github.com/yourorg/order_manager/issues",
        "Source": "https://github.com/yourorg/order_manager",
    },
)
