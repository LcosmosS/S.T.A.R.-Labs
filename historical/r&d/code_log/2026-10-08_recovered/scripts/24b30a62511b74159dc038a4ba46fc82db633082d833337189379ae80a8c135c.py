from setuptools import setup, find_packages

setup(
    name="acsc",
    version="0.0.0",
    description="ACSC utilities",
    packages=find_packages(include=["acsc", "acsc.*"]),
    include_package_data=True,
    install_requires=[
        "numpy>=1.26.0,<2.0",
        "pandas>=2.2.0,<3.0",
        "scipy>=1.11.0,<2.0",
    ],
    extras_require={
        "tda": ["gudhi==3.5.1", "ripser==0.6.2", "persim==0.6.0"],
        "dev": ["pytest", "black", "isort"],
    },
)
