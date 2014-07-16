from distutils.core import setup, Extension
import numpy.distutils.misc_util

setup(
    ext_modules=[Extension("_Quadtree", ["_Quadtree.c", "quadtree.c", "list.c"])],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)
