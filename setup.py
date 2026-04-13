#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup script for nnids_pipeline minimal package."""

from setuptools import setup, find_packages

setup(
    name="nnids-pipeline-minimal",
    version="0.1.0",
    description="Minimal autonomous NNIDS ingestion pipeline",
    packages=find_packages(include=["core", "core.*", "configs", "configs.*"]),
    include_package_data=True,
    install_requires=[
        "boto3>=1.28.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "PyYAML>=6.0",
    ],
    python_requires=">=3.10",
)
