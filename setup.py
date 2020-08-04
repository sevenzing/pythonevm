from setuptools import setup, find_packages

setup(
    name="pythonevm",
    version="1.0",
    packages=find_packages(exclude=['tests.*']),
    
    author="Lymarenko Lev",
    author_email="lymarenko.lev@gmail.com",
    
    description="Emulation ethereum virtual machine",
    keywords="evm pyevm ethereum virtual machine",
    
    long_description='README.md'
)