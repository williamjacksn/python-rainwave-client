from setuptools import setup

import rainwaveclient

setup(
    name='python-rainwave-client',
    version=rainwaveclient.__version__,
    author=rainwaveclient.__author__,
    author_email='william@subtlecoolness.com',
    url='https://github.com/williamjacksn/python-rainwave-client',
    description='Python client library for Rainwave',
    packages=['rainwaveclient'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries'
    ],
    license=open('LICENSE').read()
)
