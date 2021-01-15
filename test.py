import re

str_inc = "wcieji+++mš$GNGGA,135618.00,5006.5952471,N,01424.0561884,E,1,08,2.15,185.775,M,44.328,M,,*4Baaa"
string = "$GNGGA,135618.00,5006.5952471,N,01424.0561884,E,1,08,2.15,185.775,M,44.328,M,,*4B"

m = re.search("\$GGNGGA.*\*..", str_inc)
print(m)
print(m.start())
print(m.end())
print(len(str_inc))

print(str_inc[m.start():m.end()])

#print(email[:m.start()] + email[m.end():])
