import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="localpackages",
    version="0.1",
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)