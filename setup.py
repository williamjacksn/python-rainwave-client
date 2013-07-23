from distutils.core import setup

import gutter

setup(
    name = u'gutter',
    version = gutter.__version__,
    author = gutter.__author__,
    author_email = u'william@subtlecoolness.com',
    url = u'https://gutter.readthedocs.org/',
    description = u'Rainwave client framework',
    packages = [u'gutter'],
    classifiers = [
        u'Development Status :: 3 - Alpha',
        u'Intended Audience :: Developers',
        u'License :: OSI Approved :: MIT License',
        u'Natural Language :: English',
        u'Programming Language :: Python',
        u'Programming Language :: Python :: 2.7',
        u'Topic :: Software Development :: Libraries'
    ],
    license = open(u'LICENSE').read()
)
