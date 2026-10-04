from setuptools import find_namespace_packages, setup


setup(
    name="star",
    version="0.1.0",
    packages=find_namespace_packages(
        where=".",
        include=["src*", "scripts*"],
    ),
)
