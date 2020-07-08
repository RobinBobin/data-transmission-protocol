from dataxmissionprotocol.version import __version__
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ],
   description="Data transmission protocol package",
   install_requires = [
      "simple-common-utils"
   ],
   long_description=long_description,
   long_description_content_type="text/markdown",
   name="dataxmissionprotocol",
   packages=find_packages(),
   url="https://github.com/RobinBobin/data-transmission-protocol",
   version=__version__
)
