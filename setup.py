from setuptools import setup, find_packages
from src.energy_meter import __VERSION__

setup(
   name='energy_meter',
   version=__VERSION__.decode("utf-8"),
   packages=find_packages(where="."),
   license='MIT',
   long_description=open('README.md').read(),
   # package_dir={"": "src"},
)
