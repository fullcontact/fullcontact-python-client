from setuptools import setup, find_packages

requirements = [
    # Test
    "pytest==5.4.1",
    # Prod
    "requests==2.23.0"
]

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="python-fullcontact",
    version="1.0.0",

    author="Nithin Subhash",
    author_email="nithin.subhash@fullcontact.com",
    
    description="A simple Fullcontact API client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/fullcontact/fullcontact-python-client",
    
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    python_requires='~=3.5',
    install_requires=requirements

)
