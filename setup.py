from __future__ import unicode_literals

import setuptools

import rainwaveclient

setuptools.setup(
    name=rainwaveclient.__setup_name__,
    version=rainwaveclient.__version__,
    author=rainwaveclient.__author__,
    author_email=rainwaveclient.__author_email__,
    url=rainwaveclient.__url__,
    description=rainwaveclient.__description__,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['rainwaveclient'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    license='MIT License',
    keywords=rainwaveclient.__keywords__
)
