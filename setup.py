import setuptools
from intry_opcua_server import version

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="intry_opcua_server",
    version=version.__version__,
    author="Gabriel Martín Blázquez",
    author_email="gmartin_b@usal.es",
    description="An OPC UA server created to simulate data acquisition from different sensors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabrielmbmb/intry4.0-opcua-server",
    packages=setuptools.find_packages(),
    data_files=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=[],
    entry_points={"console_scripts": ["intry-opcua = intry_opcua_server.__main__:main"]},
)
