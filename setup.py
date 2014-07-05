from distutils.core import setup, Extension

setup(
    ext_modules=[Extension("_norm", ["_norm.c", "norm.c"])]
)
