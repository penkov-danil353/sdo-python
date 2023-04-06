from setuptools import Extension, setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(Extension(
           "parsewrapper",                                # the extension name
           sources=["parsewrapper.pyx", "library.cpp"],   # the Cython source additional C++ source files
           language="c++",                                # generate and compile C++ code
      )))
