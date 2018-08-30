
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(name="honen",
      version="0.1",
      author="moskomule",
      author_email="hataya@nlab.jp",
      packages=["honen"],
      url="https://github.com/moskomule/honen",
      description="matplotlib wrapper",
      long_description=readme,
      license="BSD",
      )
