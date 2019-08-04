# -*- coding: utf-8 -*-

import setuptools

setuptools._install_setup_requires({'setup_requires': ['git-versiointi']})
from versiointi import asennustiedot

setuptools.setup(
  name='testarossa',
  description='Oikopolkuja Python-yksikkötestautukseen',
  url='https://github.org/an7oine/testarossa',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@me.com',
  packages=setuptools.find_packages(),
  include_package_data=True,
  zip_safe=False,
  **asennustiedot(__file__),
)
