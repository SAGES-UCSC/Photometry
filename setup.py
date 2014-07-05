from distutils.core import setup, Extension

setup(
    ext_modules=[Extension("_norm", ["_norm.c", "norm.c"]),
                 Extension("_angular_dist", ["_angular_dist.c", "angular_dist.c"])]
)
