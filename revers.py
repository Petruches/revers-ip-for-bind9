#!python3.12
import sys

count = sys.argv[1]

for i in range(int(count)):
    ip=input("Введите ip:\n").split('.')
    ip.reverse()
    record = '.'.join(ip) + ".in-addr.arpa."
    file = open(sys.argv[4], 'a')
    file.write(record.ljust(54) + f"{sys.argv[2]}   IN  PTR    " + sys.argv[3] + "." + '\n')
    file.close()
