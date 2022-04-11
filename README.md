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
-f | --ftp       : přístupové údaje na ftp server, formát  <server_adress>|<user_name>|<password> (defaultně None)
```

příklad spuštění :

```bash
python3 main.py -p /dev/ttyACM0 -b 38400 -d .
```

TODO: 
* mazání zasynchronizovanych dat 
* opakované odesílání - např. výpadek internetu
* logování eventů do souboru
