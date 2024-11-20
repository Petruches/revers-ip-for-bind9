#!python3.12

count = int(input("Введите количество ip: "))

for i in range(count):
    ip=input("Введите ip:\n").split('.')
    ip.reverse()
    print("PTR: " + '.'.join(ip) + ".in-addr.arpa.")
