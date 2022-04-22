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

Nastaveni crontabu :

```bash
crontab -e

#vložení řádku - testování běhu skriptu každou minutu
*/1 * * * * pgrep GnssLogger > /dev/null || cd ~/Repos/GNSS-logger && python3 main.py -p /dev/ttyACM0 -b 38400 -f <server_adress>::<user_name>::<password>
```

TODO:

- mazání zasynchronizovanych dat po X měsících (asi další skript)
