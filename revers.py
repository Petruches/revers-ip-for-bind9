#!python3.12
import sys
import getopt


def tail(fnam: str, k: int):
    with open(fnam,"r") as fi:
        txt=fi.readlines()
        count=len(txt)
        for i in range(count-k,count):
            print(txt[i],end='')


def hlp(arg):
    try:
        opts, args = getopt.getopt(arg, 'h', ['help'])
    except getopt.GetoptError as err:
        print(err) # print "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            print("""Usage: python hello.py [OPTION]... [arg]: [count] [timeout] [name] [file]

  -h, --help                      display this help and exit

  Report bugs to <petryches.99@gmail.com>
    """)
            sys.exit()
        else:
            assert False, 'unhandled option'


def main():
    hlp(sys.argv[1:])
    count = sys.argv[1]
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