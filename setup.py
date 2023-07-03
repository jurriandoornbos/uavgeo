import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uavgeo",
    version="0.0.rev0",
    author="Jurrian Doornbos",
    author_email="jurriandoornbos@gmail.com",
    description="UAV image processing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jurriandoornbos/uavgeo/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Pre-processors"

    ],
    python_requires='>=3.9',
)