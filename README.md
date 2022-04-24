# GNSS-logger

instalace potřebných balíčků :

```bash
pip3 install -r requirements.txt
```

parametry :

```bash
-h |             : nápověda
-p | --port_name : specifikace sériového portu
-b | --baudrate  : nastavení rychlosti komunikace seriového portu (defaultně 38400)
-d | --directory : specifikováni nazvu projektu do jehož slozky se budou data ukládat (defaultně "Test")
-f | --ftp       : přístupové údaje na ftp server, formát  <server_adress>::<user_name>::<password> (defaultně None)
-e | --erase     : vymazání lokálních souborů, po úspěšném nahrání na FTP server
```

příklad spuštění :

```bash
python3 main.py -p /dev/ttyACM0 -b 38400 -d .
```

Nastavení zpráv U-blox přijímače:

- RXM-RAWX
- RXM-SFRBX
- NMEA-ZDA

## Nastaveni crontabu :

```bash
crontab -e

#vložení řádku - testování běhu skriptu každou minutu
*/1 * * * * pgrep GnssLogger > /dev/null || cd ~/Repos/GNSS-logger && python3 main.py -p /dev/ttyACM0 -b 38400 -f <server_adress>::<user_name>::<password>
```

## Spouštění zkompilovaného programu:

Zkompilovaný program lze stáhnout ze záložky actions, popřípadě v Realeses.
Spouštění probíhá podobně, jen není nutné instalovat knihovny.

```bash
./GnssLogger -p /dev/ttyACM0 -b 38400 -d .
```

Obdobně je nutné upravit i název v crontabu.

## Průběžné promazávání souborů:

Aby nedošlo k přeplnění paměti na počítači, je zde přiložen skript "test_and_delete.py":

```bash
python3 test_and_delete.py
-h |        : nápověda
-d | --days : Soubory ve složkách LOGS a RINEX, které byly naposledy upraveny déle než je stanovený počet dnů budou vymazány. Defaultně 30 dnů.
```

Tuto úlohu je možné automatizovat v cronu, např. vymazání souborů naposledy upraveny před déle než 45 dny s kontrolou každý den v 0:00.

```bash
crontab -e

0 0 */1 * * cd ~/Repos/GNSS-logger && python3 test_and_delete.py --days 45
```
