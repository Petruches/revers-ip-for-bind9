#!python3.12
import sys

count = sys.argv[1]

for i in range(int(count)):
    ip=input("Введите ip:\n").split('.')
    ip.reverse()
    record = '.'.join(ip) + ".in-addr.arpa."
    file = open(sys.argv[3], 'a')
    file.write(record.ljust(54) + "3600   IN  PTR    " + sys.argv[2] + "." + '\n')
    file.close()
