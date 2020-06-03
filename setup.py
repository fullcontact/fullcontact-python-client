from setuptools import setup, find_packages

from fullcontact.__about__ import *

requirements = [
    # Test
    "pytest==5.4.1",
    # Prod
    "requests==2.23.0",
    "urllib3==1.25.7"
]

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name=__name__,
    version=__version__,

    author=__author__,
    author_email=__author_email__,

    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/fullcontact/fullcontact-python-client",

    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    python_requires='~=3.5',
    install_requires=requirements,
    license=__license__
)
