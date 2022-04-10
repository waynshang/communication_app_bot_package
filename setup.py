from setuptools import setup, find_packages
import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

classifier = [
  'Development Status :: Production',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'programming Language :: Python :: 3.8'
]

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
  name='communicationAppModule',
  version="0.1.1",
  description='Module to connect with communication app and send message',
  long_description="%s\n%s" % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.txt'))
    ),
  long_description_content_type="text/markdown",
  author='Wayne Shang',
  author_email='wayne18308@gmail.com',
  license='MIT',
  classifier=classifier,
  keywords='Communication App',
  packages=find_packages(),
  install_requires=['']
)