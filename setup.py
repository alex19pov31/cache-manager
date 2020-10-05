from setuptools import setup, find_packages
import proxy_parser

setup(
    name="proxy_parser",
    version=proxy_parser.__version__,
    packages=find_packages(),
    author="Alexander Nesterov",
    author_email="alex19pov31@gmail.com",
    license="MIT"
)