# GNSS-logger

instalace potřebných balíčků :

```bash
pip install -r requirements.txt
```

parametry :

```bash
-h               : nápověda
-p | --port_name : specifikace sériového portu
-b | --baudrate  : nastavení rychlosti komunikace seriového portu
```

příklad spuštění :

```bash
python3 main.py -p /dev/ttyACM0 -b 38400
```
