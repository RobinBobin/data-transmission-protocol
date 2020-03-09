import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   name="dataxmissionprotocol",
   version="1.1.1",
   author="Ruben Shalimov",
   author_email="r_shalimov@inbox.ru",
   description="Data transmission protocol package",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/RobinBobin/data-transmission-protocol",
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent"
   ]
)
