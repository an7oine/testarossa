#!/usr/bin/env python
## -*- coding: utf-8 -*-
# vi: et sw=2 fileencoding=utf-8
# pylint: disable=protected-access, invalid-name

import functools
import inspect
import sys
import unittest

from .laajennos import laajennokset


def testarossa_testit(moduuli, loader, tests, pattern):
  '''
  Palauta moduulin `self` sisältämät Testarossa-testiaineistot
  `unittest.TestSuite`-pakettina.
  '''
  # pylint: disable=unused-argument
  return loader.suiteClass(
    loader.loadTestsFromTestCase(
      type(
        testi.pop('__name__'),
        (testi.pop('__class__'), )
        if testi.get('__class__') else (unittest.TestCase, ),
        testi,
      )
    )
    for testi in map(laajennokset, moduuli._testarossa)
  )
  # def testarossa_testit


def lisaa_testi(*, nayte, koe, **kwargs):
  '''
  Lisää annetun `naytteen` sisältävän moduulin `_testarossa`-
  määreeseen uusi testi siten, että `testi.nayte` on annettu näyte ja
  `testi.koe` on annettu koe tai kokeet.

  Lisää moduuliin tarvittaessa `load_tests`-funktio, joka muodostaa
  testipaletin (`unittest.TestSuite`) em. `_testarossa`-määreen
  mukaisesti. Ks.
  https://docs.python.org/3/library/unittest.html#load-tests-protocol
  '''
  _nayte = nayte.__func__ if inspect.ismethoddescriptor(nayte) else nayte
  if getattr(_nayte, '__module__', None):
    moduuli = sys.modules[_nayte.__module__]
  elif getattr(koe, '__module__', None):
    moduuli = sys.modules[koe.__module__]
  else:
    raise ValueError(
      'Joko näytteen tai kokeen on viitattava johonkin Python-moduuliin!'
    )
  moduuli.__dict__.setdefault('_testarossa', [])
  moduuli._testarossa.append(dict(
    # Asetetaan testin moduuliksi näytteen moduuli.
    __module__=_nayte.__module__,
    # Poimitaan nimi; oletusarvo näytteen mukaan.
    __name__=kwargs.pop('__name__', _nayte.__name__),
    # Alkuperäinen näyte.
    _nayte=nayte,
    # Muodostetaan määre, joka palauttaa ajonaikaisesti
    # testattavan näytteen.
    nayte=property(lambda self: nayte),
    **(
      {'__class__': koe} if isinstance(koe, type)
      else koe if isinstance(koe, dict)
      else {
        'test_' + (getattr(koe, '__name__', None) or ''): koe,
      }
    ),
    **kwargs,
  ))
  if not hasattr(moduuli, 'load_tests'):
    moduuli.load_tests = functools.partial(testarossa_testit, moduuli)
  # def lisaa_testi


def koriste(*args, **kwargs):
  '''
  Palauta koriste, joka lisää sille annettuun funktioon, metodiin tai
  luokkaan (`nayte`) liittyvän, `kwargs`-parametrien mukaisen
  Testarossa-testiaineiston annetun kohteen sisältävän moduulin
  `_testarossa`-määreeseen.
  '''
  # pylint: disable=no-else-return
  if len(args) == 1 and not kwargs:
    # Salli oikopolku:
    # @testarossa    -->    @testarossa()
    # def ...               def ...
    return koriste()(*args)

  elif args:
    raise ValueError(
      'Vain nimetyt parametrit sallitaan.'
    )

  elif 'koe' in kwargs and 'nayte' in kwargs:
    # Näyte ja testi on annettu; lisää testi sellaisenaan.
    return lisaa_testi(**kwargs)

  elif 'koe' not in kwargs and 'nayte' in kwargs:
    # Näyte on annettu; palautetaan yksinkertainen koriste,
    # joka ottaa kokeen ja lisää testin.
    def koristeltu_koe(koe):
      # pylint: disable=missing-kwoa
      return lisaa_testi(koe=koe, **kwargs)
    return koristeltu_koe

  elif 'koe' in kwargs and 'nayte' not in kwargs:
    # Koe on annettu; palautetaan yksinkertainen koriste,
    # joka ottaa näytteen ja lisää testin.
    def koristeltu_nayte(nayte):
      # pylint: disable=missing-kwoa
      lisaa_testi(nayte=nayte, **kwargs)
      return nayte
    return koristeltu_nayte

  else: #if 'koe' not in kwargs and 'nayte' not in kwargs:
    # Näytettä eikä koetta ei ole annettu;
    # palauta koriste (1), joka ottaa kokeen ja palauttaa uuden
    # koristeen (2), joka ottaa valinnaisena lisää nimettyjä
    # parametrejä (ylikirjoittaen alkuperäisen funktiokutsun
    # parametrit) ja palauttaa uuden koristeen (3),
    # joka ottaa näytteen ja lisää testin.
    def koristeltu_koe(koe):
      def koristele_nayte(*args2, **kwargs2):
        if len(args2) == 1 and not kwargs2:
          return lisaa_testi(nayte=args2[0], koe=koe, **kwargs)
        elif args2:
          raise ValueError(
            'Vain nimetyt parametrit sallitaan.'
          )
        else:
          def koristeltu_nayte(nayte):
            lisaa_testi(nayte=nayte, koe=koe, **{**kwargs, **kwargs2})
            return nayte
          koristeltu_nayte.__name__ = koe.__name__
          return koristeltu_nayte
        # def koristele_nayte
      return koristele_nayte
    return koristeltu_koe
  # def koriste
