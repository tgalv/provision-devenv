
from setuptools import setup


setup(name="provision_devenv",
      version = '0.1',
      packages= ['provision_devenv'],
      install_requires = ["fabric", "jinja2"],
      setup_requires = ["py2exe"],
      console = ['provision_devenv/main.py'])
