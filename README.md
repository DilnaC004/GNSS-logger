# GNSS-logger

instalace potřebných balíčků :

```bash
pip install -r requirements.txt
```

parametry :

```bash
-h               : nápověda
-p | --port_name : specifikace sériového portu
-b | --baudrate  : nastavení rychlosti komunikace seriového portu (defaultně 38400)
-d | --directory : specifikováni nazvu projektu do jehož slozky se budou data ukládat (defaultně "Test")
-f | --ftp       : přístupové údaje na ftp server, formát  <server_adress>::<user_name>::<password> (defaultně None)
```

příklad spuštění :

```bash
python3 main.py -p /dev/ttyACM0 -b 38400 -d .
```

Nastavení zpráv U-blox přijímače:
* RXM-RAWX
* RXM-SFRBX
* NMEA-ZDA

Nastaveni crontabu :

```bash
crontab -e

#vložení řádku - testování běhu skriptu každou minutu 
*/1 * * * * pgrep GnssLogger > /dev/null || cd <cest_k_slozce_s_loggerem> && python3 main.py -p /dev/ttyACM0 -b 38400
```


TODO: 
* mazání zasynchronizovanych dat 
* opakované odesílání - např. výpadek internetu
