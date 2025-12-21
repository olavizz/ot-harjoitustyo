# Ohjelmistotekniikka, harjoitustyö

Toteutan *budjetointisovelluksen*, jossa käyttäjä voi hallita omaa **talouttaan** seuraamalla **tuloja** ja **menoja**.

## Asennus

1. Asenna riippuvuudet komennolla

```bash
poetry install
```

2. Käynnistä sovellus komennolla

```bash
poetry run invoke start
```

## Komennot

### Tietokannan alustus

```bash
python3 src/db_helper.py
```

### Ohjelman suoritus

```bash
poetry run invoke start
```

### Testien suoritus

```bash
poetry run invoke tests
```

### Testi raportin generointi

```bash
poetry run invoke coverage-report
```
