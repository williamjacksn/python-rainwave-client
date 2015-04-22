from __future__ import unicode_literals

from setuptools import find_packages, setup

import rainwaveclient

setup(
    name=rainwaveclient.__setup_name__,
    version=rainwaveclient.__version__,
    author=rainwaveclient.__author__,
    author_email=rainwaveclient.__author_email__,
    url=rainwaveclient.__url__,
    description=rainwaveclient.__description__,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries'
    ],
    license=open('LICENSE').read(),
    keywords=rainwaveclient.__keywords__
)
