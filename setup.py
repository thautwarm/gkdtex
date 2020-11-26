from setuptools import setup, find_packages
from pathlib import Path

with Path('README.md').open() as readme:
    readme = readme.read()

version = 0.2

setup(
    name='gkdtex',
    version=version if isinstance(version, str) else str(version),
    keywords="LaTeX, TeX, typesetting, preprocessing, programming language",
    # keywords of your project that separated by comma ","
    description="A programmable TeX-compatible 2-stage typesetting language.",  # a conceise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.7.0',
    url='https://github.com/thautwarm/gkdtex',
    author='thautwarm',
    author_email='twshere@outlook.com',
    packages=find_packages(),
    entry_points={"console_scripts": ["gkdtex=gkdtex.cli:main"]},
    install_requires=['wisepy2 >= 1.0'],
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)

