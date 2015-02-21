from setuptools import setup, find_packages
from codecs import open
from os import path
import re

BASE_DIR = path.abspath(path.dirname(__file__))

# set long description from readme file
with open(path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# set version from init file
with open(path.join(BASE_DIR, 'djenealogy', '__init__.py'), encoding='utf-8') as f:
    version = re.search("^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)


setup(
    name='djenealogy',
    version=version,

    description='Convert Gedcom files into Django models.',
    long_description=long_description,
    url='https://github.com/mheppner/django_family',
    author='Mark Heppner',
    author_email='heppner.mark@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='family gedcom ancestry genealogy',
    packages=find_packages(),
    install_requires=[
        'Django>=1.7',
        'gedcompy'
    ],
    package_data={},
    zip_safe=False,
)
