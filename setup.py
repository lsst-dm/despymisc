import distutils
from distutils.core import setup

# The main call
setup(name='despymisc',
      version ='0.2.0',
      license = "GPL",
      description = "A set of handy Python-only simple utility functions for DESDM",
      author = "NCSA",
      author_email = "felipe@illinois.edu",
      packages = ['despymisc'],
      package_dir = {'': 'python'},
      data_files=[('ups',['ups/despymisc.table'])],
      )

