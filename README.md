testarossa
==========

Python-yksikkötestausväline.

Kaksi käyttötapaa:
```python
...
@testarossa(
  koe=lambda self: self.assertEqual(self.nayte(1, 2), 3),
  ...
)
def funktio_jota_testataan(x, y):
  return x + y
...
```

Tai:
```python
@testarossa(
  ...
)
def laske_yksi_plus_kaksi(self):
  self.assertEqual(self.nayte(1, 2), 3)
...

@laske_yksi_plus_kaksi
def funktio_jota_testataan(x, y):
  return x+y
```

Lisäksi seuraava lyhennysmerkintä on mahdollinen:
```python
...
@testarossa
def funktio_joka_saattaa_kaatua(x=0):
  return int(x)
...
```
