from setuptools import find_packages
from setuptools import setup,Extension

setup(name="bib2doi",
      version="1.0.0",
      packages=find_packages(),
      description="Package for finding DOI for bibtex bibliography",
      url="https://github.com/zachary-hawk/bib2doi.git",
      author="Zachary Hawkhead",
      author_email="zachary.hawkhead@ymail.com",
      license="MIT",
      install_requires=["numpy",
                        "Levenshtein",
                        "bibtexparser",
                        "argparse",
                        "habanero"],

      entry_points={"console_scripts":["bib2doi=src.mainbib:main_bib",]
                    }

      )


