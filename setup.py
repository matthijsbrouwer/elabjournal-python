from setuptools import setup, find_packages

setup(
    name="elabjournal",
    version="0.0.1",
    author="Matthijs Brouwer",
    packages=find_packages(),
    license="Apache License 2.0",
    long_description=open("README.md").read(),
    install_requires=[
        "requests >= 2.21.0",
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

