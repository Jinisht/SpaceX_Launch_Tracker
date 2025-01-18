from setuptools import setup, find_packages

requirements = ["requests", "pandas"]
setup(
    name="SpaceX_Launch_Tracker",
    version="1.0.0",
    description="SpaceX_Launch_Tracker software",
    packages=find_packages(),
    install_requires=requirements
)
