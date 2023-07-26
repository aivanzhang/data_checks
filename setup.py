import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="data_checks",
    version="0.1",
    description="Data observability checks to easily create comprehensive data quality tests",
    url="https://github.com/SuperiorityComplex/data-checks",
    author="SuperiorityComplex",
    author_email="ivanzhangofficial@gmail.com",
    license="MIT",
    packages=["data_checks"],
    zip_safe=False,
    long_descp=README,
    long_descp_content="text/markdown",
)
