#!/usr/bin/python
# vi: et sw=2 fileencoding=utf-8
# pylint: disable=invalid-name

import functools

import pkg_resources


@functools.total_ordering
class Laajennos:
  def __init__(self, laajennos):
    self.nimi, self.laajennos = laajennos.name, laajennos.load()
    self.laajennos.__dict__.setdefault('ennen', ())
    self.laajennos.__dict__.setdefault('jalkeen', ())
    if self.laajennos.ennen == '__all__':
      self.laajennos.ennen = type(
        'Kaikki', (), {'__contains__': lambda *args: True}
      )()
    if self.laajennos.jalkeen == '__all__':
      self.laajennos.jalkeen = type(
        'Kaikki', (), {'__contains__': lambda *args: True}
      )()
  def __lt__(self, laajennos):
    return self.nimi in laajennos.laajennos.jalkeen \
    or laajennos.nimi in self.laajennos.ennen
  def __eq__(self, laajennos):
    return self.nimi not in laajennos.laajennos.ennen \
    and self.nimi not in laajennos.laajennos.jalkeen \
    and laajennos.nimi not in self.laajennos.ennen \
    and laajennos.nimi not in self.laajennos.jalkeen
  def __call__(self, *args, **kwargs):
    return self.laajennos(*args, **kwargs)
  # class Laajennos


_laajennokset = None
def laajennokset(testi):
  global _laajennokset
  if _laajennokset is None:
    _laajennokset = sorted(map(Laajennos, pkg_resources.iter_entry_points(
      'testarossa.laajennos'
    )))
  for laajennos in _laajennokset:
    testi = laajennos(testi)
  return testi
