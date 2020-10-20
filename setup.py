from setuptools import setup
from setuptools import find_packages
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    # Name of the package
    name='MonitoringByPing',

    # Packages to include into the distribution
    packages=find_packages('.'),

    version='1.0.0',

    license='MIT',

    # Short description of your library
    description='Monitor the devices by using ping command',

    # Long description of your library
    long_description = long_description,


    # Your name
    author='jegneshgehlot',

    # Your email
    author_email='gehlot.jegnesh@gmail.com',

    # Either the link to your github or to your website
    url='',

    # Link from which the project can be downloaded
    download_url='',

    # List of keyword arguments
    keywords=[],

    # List of packages to install with this one
    install_requires=['appdata','attrs','Click','click-default-group','importlib-metadata','iniconfig','loguru',
                        'numpy','packaging','pandas','pluggy','py','pyparsing','pytest','python-dateutil','pytz',
                        'setup-py-cli','six','toml','zipp'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
    package_data={'': ['*.csv','*.json']},
)
