from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()
    print(required)

setup(
    name='bitsandbobs',
    version='0.0.1',
    description='Personal utilities for boilerploate I use a lot',
    author='Casey Schneider-Mizell',
    author_email='caseysm@gmail.com',
    packages=["bitsandbobs"],
)
