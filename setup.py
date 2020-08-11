from distutils import ccompiler
from distutils import _msvccompiler
import os
import setuptools
import shutil
import sys


scriptdir = os.path.abspath(os.path.dirname(sys.argv[0]))
pyuipc_pyd = os.path.join(scriptdir, "fsuipc_airspaces", "pyuipc.cp38-win32.pyd")


with open("README.md", "r") as fh:
    long_description = fh.read()


class DummyCompiler(ccompiler.CCompiler):
    """A dummy compiler class.

    This does not do anything when compiling, and it copies an already existing
    pyuipc.pyd file when linking."""
    def __init__(self, verbose=0, dry_run=0, force=0):
        """Construct the compiler."""
        pass

    def compile(self, sources, output_dir=None, macros=None,
                include_dirs=None, debug=0, extra_preargs=None,
                extra_postargs=None, depends=None):
        """Just return a list of .o files from the .cc files."""
        return [source.replace(".cc", ".o") for source in sources]

    def link(self, target_desc, objects, output_filename, output_dir=None,
             libraries=None, library_dirs=None, runtime_library_dirs=None,
             export_symbols=None, debug=0, extra_preargs=None,
             extra_postargs=None, build_temp=None, target_lang=None):
        """Copy the pyuipc.pyd file to its final location."""
        if output_dir is None:
            output_dir = os.path.dirname(output_filename)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        shutil.copyfile(pyuipc_pyd, output_filename)


_msvccompiler.MSVCCompiler = DummyCompiler


setuptools.setup(
    name="fsuipc-airspaces",
    version="1.0.0",
    author="Tim Jensen",
    author_email="tim.l.jensen@gmail.com",
    description="FSUIPC client for reporting flight simulator aircraft positioning to Airspaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/tjensen/fsuipc-airspaces",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment :: Simulation"
    ],
    python_requires=">=3.8,<3.9",
    setup_requires=["wheel"],
    ext_package="fsuipc_airspaces",
    ext_modules=[setuptools.Extension("pyuipc", [])],
    entry_points={
        "console_scripts": [
            "fsuipc_airspaces = fsuipc_airspaces.fsuipc_airspaces:main"
        ]
    }
)
