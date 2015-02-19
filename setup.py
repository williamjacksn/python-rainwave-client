from setuptools import setup

import rainwaveclient

setup(
    name='python-rainwave-client',
    version=rainwaveclient.__version__,
    author=rainwaveclient.__author__,
    author_email='william@subtlecoolness.com',
    url='https://gutter.readthedocs.org/',
    description='Python Rainwave client library',
    packages=['rainwaveclient'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    license=open('LICENSE').read()
)
