from setuptools import setup, find_packages

exec(open("elabjournal/_version.py").read())

setup(
    name="elabjournal",
    version=__version__,
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

