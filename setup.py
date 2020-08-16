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
    package_data={"fsuipc_airspaces": ["py.typed"]},
    zip_safe=False,  # Enables mypy to find the installed package
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Games/Entertainment :: Simulation"
    ],
    python_requires=">=3.6",
    install_requires=["fsuipc==1.0.1"],
    entry_points={
        "console_scripts": [
            "fsuipc_airspaces = fsuipc_airspaces.fsuipc_airspaces:main"
        ]
    }
)
