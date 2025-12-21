# Testaus
Testaus on tehty tässä projektissa automatisoiduin integraatiotestein unittest-kirjaston avulla ja järjestelmätestit ovat tehty manuaalisesti. Testit sijaitsevat hakemistossa `tests/`. Testit on suunniteltu kattamaan sovelluksen keskeiset toiminnot, kuten käyttäjän rekisteröityminen, kirjautuminen, tehtävien lisääminen, muokkaaminen ja poistaminen sekä tietokantayhteyksien toimivuus.

## Testauskattavuus

Testauskattavuus on yli 60% ja se on mitattu `coverage`-työkalulla, ja kattavuusraportti voidaan generoida suorittamalla komento:

```bash
poetry run invoke coverage-report
```

Testaamatta ovat jääneet ui-luokat sekä tietokannan luonnista vastuussa oleva db_helper.py
