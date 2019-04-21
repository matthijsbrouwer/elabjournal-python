from setuptools import setup, find_packages

setup(
    name="elabjournal",
    version="0.0.6",
    author="Matthijs Brouwer",
    url="https://github.com/matthijsbrouwer/elabjournal-python",
    packages=find_packages(),
    license="Apache License 2.0",
    long_description=open("README.txt").read(),
    install_requires=[
        "requests >= 2.18.4",
        "pandas",
        "keyring",
        "IPython",
        "rjson",
        "xlrd",
        "matplotlib",
        "Pillow",
        "ipywidgets"
    ],
    classifiers=[
        "Framework :: Jupyter",
        "Intended Audience :: Science/Research",
    ],
)

