import os
from setuptools import setup


SETUP_REQUIRES = []
if not os.name == 'posix':
    SETUP_REQUIRES = ["py2exe"]

setup(name="provision_devenv",
      version = '0.1',
      packages= ['provision_devenv'],
      install_requires = ["fabric", "jinja2"],
      setup_requires = SETUP_REQUIRES,
      console = ['provision_devenv/main.py'])
