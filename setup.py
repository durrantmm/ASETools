import sys, os
from distutils.core import setup

if sys.version_info < (3,5):
    sys.exit('Sorry, Python < 3.5 is not supported')

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='asetools',
      version='1.0',
      description='Python pipeline and analysis tools to perform ASE and differential ASE analysis.',
      author='Matt Durrant',
      author_email='mdurrant@stanford.edu',
      license = "BSD",
      keywords = "genomics allele specific expression pipeline",
      url="http://packages.python.org/asetools",
      packages=['sys', 'pysam', 'vcf', 'argparse', 'recordclass', 'numpy', 'util', 'tables'],
      long_description=read('README.md')
     )