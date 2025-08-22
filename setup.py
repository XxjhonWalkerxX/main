#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="tutor-customregistration",
    version="1.0.0",
    description="Tutor plugin for custom registration fields in Open edX",
    long_description="Plugin that adds Mexican-specific custom fields to Open edX registration form",
    author="Diego Nicolas",
    author_email="diego@example.com",
    url="https://github.com/tu-usuario/tutor-customregistration",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "tutor>=19.0.0,<20.0.0",
    ],
    entry_points={
        "tutor.plugin.v1": [
            "customregistration = tutorcustomregistration.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
