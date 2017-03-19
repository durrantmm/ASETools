import sys, os
from distutils.core import setup

if sys.version_info < (3,5):
    sys.exit('Sorry, Python < 3.5 is not supported')

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='asetools',
      version='1.0',
      description='Python subprocess and process tools to perform ASE and differential ASE process.',
      author='Matt Durrant',
      author_email='mdurrant@stanford.edu',
      license = "BSD",
      keywords = "genomics allele specific expression subprocess",
      url="http://packages.python.org/asetools",
      packages=['asetools'], requires=['numpy', 'scipy', 'pysam']
      )