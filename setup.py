from distutils.core import setup

setup(name='ASETools',
      version='1.0',
      description='Python tools to perform ASE and differential ASE analysis.',
      author='Matt Durrant',
      author_email='mdurrant@stanford.edu',
      url='www.stanford.edu',
      packages=['sys', 'pysam', 'vcf', 'argparse'],
     )