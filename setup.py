import distutils
from distutils.core import setup
import glob

bin_files = glob.glob("bin/*.py")
#bin_files = bin_files + glob.glob("bin/*.txt")

# The main call
setup(name='despymisc',
      version='1.0.3',
      license="GPL",
      description="A set of handy Python-only simple utility functions for DESDM",
      author="Felipe Menanteau, Michelle Gower",
      author_email="felipe@illinois.edu",
      packages=['despymisc'],
      package_dir={'': 'python'},
      scripts=bin_files,
      data_files=[('ups', ['ups/despymisc.table'])],
      )
