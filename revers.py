#!python3.12
import sys
import getopt
import re


PATTERN = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"

def tail(fnam: str, k: int):
    try:
        with open(fnam,"r") as fi:
            txt=fi.readlines()
            count=len(txt)
            for i in range(count-k,count):
                print(txt[i],end='')
    except Exception as a:
        print(a)


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
            check_pattern = re.search(PATTERN, str('.'.join(ip)))
            if check_pattern:
                print("############", "Check successfully", check_pattern.group(), "############")
            else:
                print("Check not successfully")
                sys.exit(1)
            file = open(sys.argv[4], 'a')
            file.write(record.ljust(54) + f"{sys.argv[2]}   IN  PTR    " + sys.argv[3] + "." + '\n')
            file.close()

            tail(sys.argv[4], 4)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
