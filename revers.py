#!python3.12
from sys import argv

count = sys.argv[1]


def tail(fnam: str, k: int):
    with open(fnam,"r") as fi:
        txt=fi.readlines()
        count=len(txt)
        for i in range(count-k,count):
            print(txt[i],end='')


def main():
    for i in range(int(count)):
        try:
            ip=input("Введите ip:\n").split('.')
            ip.reverse()
            record = '.'.join(ip) + ".in-addr.arpa."
            file = open(sys.argv[4], 'a')
            file.write(record.ljust(54) + f"{sys.argv[2]}   IN  PTR    " + sys.argv[3] + "." + '\n')
            file.close()
            tail(sys.argv[4], 4)
        except Exeption as e:
            print(e)


if __name__ == '__main__':
    main()