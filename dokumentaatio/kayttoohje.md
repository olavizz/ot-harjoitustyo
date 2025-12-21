# Käyttöohje
Kloonaa projekti GitHubista omaan koneeseesi komennolla:

```bash
git clone
```
## Ohjelman käynnistäminen
Asenna ensin riippuvuudet komennolla:

```bash
poetry install
```

Alusta tietokanta suorittamalla `db_helper.py`-tiedosto:

```bash
python3 src/db_helper.py
```

Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Sovelluksen käyttö
Sovelluksen käynnistyttyä näet kirjautumisnäytön. Voit joko kirjautua sisään olemassa olevalla käyttäjätunnuksella tai rekisteröityä uudeksi käyttäjäksi.

### Rekisteröityminen
1. Klikkaa "Register" -painiketta.
2. Täytä vaaditut tiedot, kuten käyttäjätunnus ja salasana.
3. Klikkaa "Register" -painiketta.
4. Palaa kirjautumisnäyttöön ja kirjaudu sisään uudella käyttäjätunnuksellasi.

### Kirjautuminen
1. Syötä käyttäjätunnus ja salasana.
2. Klikkaa "Login" -painiketta.
3. Jos tiedot ovat oikein, pääset sovelluksen päävalikkoon
4. Voit kirjautua ulos klikkaamalla "Logout" -painiketta päävalikosta.

### Tulojen ja menojen hallinta
- Voit lisätä tuloja kirjoittamalla kenttään summan ja klikkaamalla "Increase"
- Voit vähentää saldoa kirjoittamalla kenttään summan ja klikkaamalla "Decrease"
- Voit lisätä menoja täyttämällä tarvittavat tiedot ja painaa Enter.
- Voit muokata tai poistaa menoja valitsemalla haluamasi meno listasta ja käyttämällä "Edit" tai "Delete" -painikkeita.
