import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bayespoker",
    version="0.1-dev",
    author="Ketan Jog",
    author_email="kj2473@columbia.edu",
    description="Bayesian Opponent Modelling for Texas Holdem Poker",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/codeprentice-org/sniffpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
