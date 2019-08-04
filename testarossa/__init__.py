# -*- coding: utf-8 -*-
# pylint: disable=protected-access

import os
import sys
import unittest

from .koriste import koriste


# Lisää TestLoader-luokan toteutukseen poikkeus, joka ottaa
# testimoduulien haussa annetun tiedostonimikuvion (test*.py)
# lisäksi huomioon myös koristeen `@testarossa` sisältävät tiedostot.
# Huomaa, että metodia kutsutaan vain kelvollisten
# python-lähdekooditiedostojen (*.py) osalta.
_match_path_ = unittest.TestLoader._match_path
def _match_path(self, path, full_path, pattern):
  if _match_path_(self, path, full_path, pattern):
    return True
  with open(full_path) as tiedosto:
    return '@testarossa' in tiedosto.read()
unittest.TestLoader._match_path = _match_path


# Salli käsillä olevan moduulin kutsuminen funktiona.
class Moduuli(sys.modules[__name__].__class__):
  __call__ = staticmethod(koriste)
sys.modules[__name__].__class__ = Moduuli


# Tarjoa unittest-moduulin sisältö osana käsillä olevaa moduulia.
sys.modules[__name__].__dict__.update(unittest.__dict__)
