testarossa
==========

Oikotie Python-yksikkötestaukseen

Testauta kehitettävää koodia suoraan sen omassa moduulissa nopeiden testauskoristeiden (decorator) avulla. Laajenna ja mukauta oletusarvoista testipalettia helposti tarvittaessa. Erllisiä testimoduuleita (test*.py) ei enää tarvita.

Testarossa on laajennettavissa sille suunniteltujen liitännäisten avulla kirjasto- ja kehitysympäristökohtaiset (esim. Django) vaatimukset ja olosuhteet huomioonottaviin testitilanteisiin. Lataa nopeasti vaikkapa testidata (Django-fixture) suoraan siellä, missä sitä käytetään.

Vaatimukset:
------------

Python 3.5+

Käyttöönotto:
-------------

```bash
pip install testarossa
```

Suorita alustuskoodi (`import testarossa`) projektityypistä ja -rakenteesta riippuen jossakin seuraavista moduuleista:
* projektin juuressa (`__init__.py`)
* testattavan paketin juuressa (`__init__.py`)
* Django: projektiasetuksissa (`settings.py` tms.)

Alustuksen yhteydessä testimoduulien hakukriteereitä (ks. `unittest.TestLoader`) muokataan ajonaikaisesti siten, että koristeen `@testarossa` sisältävät python-moduulit käsitellään (tavanomaisten, `test*.py`-nimisten lisäksi) testimoduuleina.

Testien kirjoittaminen osaksi tuotantomoduulia:
-----------------------------------------------

Moduuli on kutsuttavissa sellaisenaan funktiona. Nimettyinä parametreinä voidaan antaa
- `nayte`: tuotantokoodin osa, jota testataan, esim.
    - funktio
    - luokka
    - jokin muu python-olio
- `koe`: ajettava testauskoodi; tämä voi olla
    - funktio: ajetaan `TestCase`-alaluokan metodina ja saa parametrinaan muuttujan `self`; 'test_' + funktion nimi asetetaan testimetodin nimeksi 
    - sanakirja: useita edellä kuvatun mukaisia testimetodeita: avainten on syytä olla 'test_'-alkuisia
    - luokka: testaamiseen käytettävä `TestCase`-alaluokka
- muita eri liitännäisten käyttämiä tai testauskoodissa huomioitavia parametrejä

Funktiokutsu:
1. mikäli sekä `nayte` että `koe` annetaan, lisätään testi sellaisenaan
2. mikäli jompi kumpi annetaan, palautetaan python-koriste ("decorator"), joka ottaa puuttuvan `kokeen` tai `naytteen` ja lisää sitten testin
3. mikäli kumpaakaan ei anneta, palautetaan koriste, joka ottaa kokeen ja palauttaa uuden koristeen (samalla nimellä kuin testi); tämä koriste ottaa näytteen ja luo lopullisen testin

Joko näytteen tai kokeen on syytä sisältää viittaus (`__module__`) omaan python-moduuliinsa; ensisijaisesti käytetään näytteen moduulia. Dynaaminen testiluokka lisätään ajonaikaisesti kyseiseen moduuliin.

Esimerkkejä:
```python
import testarossa

...
# Tapa 1: näyte ja ajettava koe annetaan suoraan koristeelle.
# Huomaa, että näin muodostettua testiä ei sellaisenaan löydetä
# python-yksikkötestien haussa ellei tiedostonimi ole `test`-alkuinen.
# Haku etsii merkkijonoa `@testarossa`, joka on syytä lisätä
# tarvittaessa kommenttina lähdekoodiin.
class Tuotanto:
  def __str__(self):
    return 'toimii'
testarossa( # @testarossa
  nayte=Tuotanto,
  koe=lambda self: self.assertEqual(str(self.nayte()), 'toimii'),
)
...

# Tapa 2a: ajettava koe annetaan suoraan koristeelle.
@testarossa(
  koe=lambda self: self.assertEqual(self.nayte(1, 2), 3),
)
def funktio_jota_testataan(x, y):
  return x + y
...

# Tapa 2b: ajettava näyte annetaan suoraan koristeelle.
def osamäärä(x, y):
  return x / y
@testarossa(nayte=laske_summa)
def voiko_nollalla_jakaa(self):
  return self.assertRaises(ZeroDivisionError, self.nayte, 1, 0)
...

# Tapa 3: testi muodostetaan ensin testarossa-koristeen avulla.
# Saadulla koristeella koristellaan jäljempänä määritelty näyte.
@testarossa(
  luvut=(1, 2),
)
def laske_yksi_ja_kaksi(self):
  self.assertEqual(self.nayte(*self.luvut), 3)
...
@laske_yksi_ja_kaksi
def funktio_jota_testataan(x, y):
  return x + y
@laske_yksi_ja_kaksi(luvut=(3, 1))
def funktio_jota_testataan(x, y):
  return x * y
```

