from setuptools import setup

setup(
    name = "weighwords",
    version = "0.2",
    author = "Lars Buitinck",
    author_email = "L.J.Buitinck@uva.nl",
    description = "Python library for creating word weights/word clouds from text",
    keywords = "word cloud nlp language model",
    license = "LGPL",
    packages = ["weighwords"],
    install_requires = ["numpy>=1.4.0"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Text Processing",
    ]
)
