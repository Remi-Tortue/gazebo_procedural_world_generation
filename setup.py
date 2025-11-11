from setuptools import setup, find_packages

setup(
    name="o2r_pi2_controllers",
    version="0.0.1",
    description="A package providing MPC controller based on acados for MM and base robots",
    author="Porée Rémi",
    author_email="remi.poree@laas.fr",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
