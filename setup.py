import os
import re
from setuptools import setup, find_packages

here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, "README.md")) as f:
    readme = f.read()
with open(os.path.join(here, "src", "__init__.py")) as f:
    version = re.search(r'__version__ = (["\'])([^"\']*)\1', f.read())[2]

setup(
    name="CanImmune",
    version=version,
    description="Neoantigen prediction tool for cancer immunotherapy.",
    long_description=readme,
    url="http://canelib.erc.monash.edu/purcell-lab",
    author="Sanjay SG Krishna",
    author_email="sanjaygowda6633@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="Neoantigen, Cancer, Immunotherapy, Tumor, Immune",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
)