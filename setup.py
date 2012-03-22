from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))

version = '0.1'
install_requires = ['BeautifulSoup']

if sys.version_info < (2,7):
    install_requires.append('argparse')
elif sys.version_info >= (3,0) and sys.version_info < (3,2):
    install_requires.append('argparse')

tests_require = ['nose']

setup(name='omcnotes',
    version=version,
    description="Build the show notes for OMC",
    long_description="",
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='podcast shownotes',
    author='Craig Maloney',
    author_email='something',
    url='http://openmetalcast.com/',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts':
            ['omcnotes=shownotes:main']
    }
)

