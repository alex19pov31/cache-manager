from setuptools import setup, find_packages
import cache_manager

setup(
    name="cache_manager",
    version=cache_manager.__version__,
    packages=find_packages(),
    author="Alexander Nesterov",
    author_email="alex19pov31@gmail.com",
    license="MIT"
)