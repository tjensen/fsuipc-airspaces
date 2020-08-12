import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


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
    python_requires=">=3.5,<3.9",
    install_requires=["fsuipc"],
    dependency_links=[
        "git+git://github.com/tjensen/fsuipc.git#egg=fsuipc"
    ],
    entry_points={
        "console_scripts": [
            "fsuipc_airspaces = fsuipc_airspaces.fsuipc_airspaces:main"
        ]
    }
)
