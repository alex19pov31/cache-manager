from setuptools import setup, find_packages
import cache_manager

with open('readme.md') as f:
    long_description = f.read()

setup(
    name="cache_manager",
    url="https://github.com/alex19pov31/cache-manager",
    version=cache_manager.__version__,
    packages=find_packages(),
    description="Simple cache manager",
    long_description=long_description,
    author="Alexander Nesterov",
    author_email="alex19pov31@gmail.com",
    license="MIT"
)