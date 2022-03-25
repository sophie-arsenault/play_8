import ast
import os
import re
import sys

import setuptools

assert sys.version_info >= (3, 6, 0), "play_8 requires Python 3.8+"


current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md"), encoding="utf8") as ld_file:
    long_description = ld_file.read()


_version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")


with open(os.path.join(current_dir, "play_8.py"), "r") as f:
    version = _version_re.search(f.read()).group("version")
    version = str(ast.literal_eval(version))


requires = [
    "flake8 > 3.0.0",
    "pytest",
]

setuptools.setup(
    name="play_8",
    license="MIT",
    version=version,
    description="an extension to flake8 to help with Playwright-specific needs",
    author="Sophie Arsenault",
    author_email="sophie@sophiecodes.com",
    url="https://github.com/sophie-arsenault/play_8",
    install_requires=requires,
    entry_points={"flake8.extension": ["PLY80 = play_8:Plugin"]},
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
