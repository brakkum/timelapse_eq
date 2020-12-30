from setuptools import setup


def read(file):
    with open(file, "r") as rm:
        return rm.read()


setup(
    name="timelapse_eq",
    version="0.1",
    description="A Python package for creating smooth EV changes in timelapse photography",
    long_description=read("README.md"),
    url="http://github.com/brakkum/timelapse_eq",
    author="Daniel Brakke",
    author_email="brakphoto@gmail.com",
    keywords="photography timelapse exposure",
    license="MIT",
    packages=["timelapse_eq"],
    install_requires=[
        "Pillow",
        "exifread",
        "rawpy",
        "colorama"
    ],
    entry_points= {
        "console_scripts": [
            "timelapse_eq = timelapse_eq.__main__:main"
        ]
    },
    include_package_data=True)
