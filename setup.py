import sys
from distutils.core import setup

if sys.version_info < (3,5):
    sys.exit('Sorry, Python < 3.5 is not supported')

setup(name='ASETools',
      version='1.0',
      description='Python tools to perform ASE and differential ASE analysis.',
      author='Matt Durrant',
      author_email='mdurrant@stanford.edu',
      url='www.stanford.edu',
      packages=['sys', 'pysam', 'vcf', 'argparse', 'recordclass'],
     )