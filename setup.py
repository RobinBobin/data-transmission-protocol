import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ],
   description="Data transmission protocol package",
   long_description=long_description,
   long_description_content_type="text/markdown",
   name="dataxmissionprotocol",
   packages=setuptools.find_packages(),
   url="https://github.com/RobinBobin/data-transmission-protocol",
   version="1.2.0"
)
