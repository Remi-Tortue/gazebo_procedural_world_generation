from setuptools import setup, find_packages

setup(
    name="gazebo_procedural_world_generation",
    version="0.0.1",
    description="A package to generate gazebo procedural worlds",
    author="Porée Rémi",
    author_email="remi.poree.pro@protonmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
