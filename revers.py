#!python3.12
import sys

count = sys.argv[1]

for i in range(int(count)):
    ip=input("Введите ip:\n").split('.')
    ip.reverse()
    print("PTR: " + '.'.join(ip) + ".in-addr.arpa.")
