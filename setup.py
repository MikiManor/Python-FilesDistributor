from setuptools import setup, find_packages
import os,sys

setup(
    name = "IvrDynMessages",
    version = "1.0",
    author="Miki Manor",
    author_email="mmanor@isracard.co.il",
    description="utility for ControlM which gets fileName, subDir and environment and delivers the files with thew same prefix to cti Servers ",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.5"
    ],
    install_requires=['UsefulUtilities'],
    python_requires='>=3',
    packages = ['IvrDynMessages'],
    entry_points={
        'console_scripts': [
            'IvrDynMessages = IvrDynMessages.__main__:main'
        ]
    },
    )

