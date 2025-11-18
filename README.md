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

Raportti löytyy htmlcov hakemistosta

# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella käyttäjä voi hallita ja tarkastella tulojaan ja menojaan. Sovellus on oman talouden seurantatyökalu, jolla voi olla useampi käyttäjä.

## Käyttäjät

Sovelluksella on aluksi vain normaalikäyttäjiä, myöhemmin saatetaan lisätä suuremmilla oikeuksilla olevia käyttäjiä.

## Toiminnallisuus

    • Käyttäjä voi rekisteröityä
    • Käyttäjä voi kirjautua sisään ja ulos
    • Käyttäjä voi lisätä omia tuloja ja menoja
    • Käyttäjä voi muokata ja poistaa itse lisäämiään tapahtumia
    • Sovellus luokittelee menot eri kategorioihin
    • Sovellus tekee tuloista ja menoista yhteenvedon
    • Sovellus näyttää käyttäjän nykyisen saldon 
    • Jokainen käyttäjä näkee vain omat tietonsa

## Mahdolliset jatkokehitykset

    • Budjetin asettaminen kuukausi- tai kategoriatasolla
    • Ilmoitus tai varoitus, jos budjetti ylittyy
    • Hakutoiminto tapahtumille
    • Tapahtumien suodatus 
