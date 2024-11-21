"""Installation file for hollerith"""
import os

import numpy
from setuptools import Extension
from setuptools import setup

if os.name == "nt":  # windows
    extra_compile_args = ["/openmp", "/O2", "/w", "/GS"]
elif os.name == "posix":  # linux/mac os
    extra_compile_args = ["-O3", "-w"]

HERE = os.path.abspath(os.path.dirname(__file__))

# Get version from version info
__version__ = None
version_file = os.path.join(HERE, "src", "_version.py")
with open(version_file, mode="r") as fd:
    # execute file from raw string
    exec(fd.read())

with open(os.path.join(HERE, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hollerith",
    packages=["hollerith"],
    package_dir={"hollerith": "src"},
    version=__version__,
    description="C-extension module for efficient writing of fixed width text",
    url="https://github.com/ansys/hollerith/",
    project_urls={
        "Documentation": "https://hollerith.docs.pyansys.com/",
        "Source": "https://github.com/ansys/hollerith/",
        "Tracker": "https://github.com/ansys/hollerith/issues",
    },
    long_description=long_description,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_dirs=[os.path.join(numpy.get_include())],
    ext_modules=[
        Extension(
            "hollerith._writer",
            [
                "src/_writer.pyx",
                "src/writer.c",
            ],
            extra_compile_args=extra_compile_args,
            language="c",
        ),
    ],
    python_requires=">=3.9",
    install_requires=["numpy>=1.26.4", "pandas>=2.0.3"],
)
