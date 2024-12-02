#!/usr/bin/env python3
import sys
import getopt
import re
import os
import logging


logging.basicConfig(level=logging.DEBUG, filename="/var/log/py_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")


class Base():

    @staticmethod
    def tail(fnam: str, k: int) -> str:
        try:
            with open(fnam,"r") as fi:
                txt=fi.readlines()
                count=len(txt)
                for i in range(count-k,count):
                    print(txt[i],end='')
        except Exception as a:
            print(a)


    @staticmethod
    def usage():
        print("""Usage: python hello.py [OPTION]... [arg]: [count] [timeout] [name] [file]

  -h, --help                      display this help and exit
  -c, --count
  -s, --select
  -j, --json

  Report bugs to <petryches.99@gmail.com>
        """)


    @staticmethod
    def check_pattern(text: str) -> str:
        search_pattern = re.search(PATTERN, text)
        if search_pattern:
            print(f"""############

            Check successfully {search_pattern.group()}

            ############""")
        else:
            print("Check not successfully")
            sys.exit(1)


    @staticmethod
    def check_dir(home: str) -> None:
        try:
            DIR_REVERS = os.path.join(home, ".revers")
            FILE_REVERS = os.path.join(home, ".revers/revers.json")
            if os.path.isdir(DIR_REVERS) and os.path.isfile(FILE_REVERS):
                print(f"\"{FILE_REVERS}\" exists")
            else:
                #print(f"\"{FILE_REVERS}\" doesn't exist\nCreating dir...")
                logging.debug(f"\"{FILE_REVERS}\" doesn't exist - Creating dir...")
                os.mkdir(DIR_REVERS)
                open(os.path.join(DIR_REVERS, FILE_REVERS), 'a').close()
                with open(os.path.join(DIR_REVERS, FILE_REVERS), 'w') as filejs:
                    filejs.write("""{
    "dirptr": "",
    "dirin": "",
    "direx": "",
    "domen": ""
}""")
                #print(f"\"{FILE_REVERS}\" created")
                logging.debug(f"\"{FILE_REVERS}\" created")
        except Exception as e:
            print(e)


class MyApp(Base):

    PATTERN = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
    HOME: str = os.path.expanduser("~")

    def __init__(self,  arg: str):
        self.arg = arg
        file: str
        select: str
        json: str


    def key_selection(self, *args) -> str:
        try:
            opts, args = getopt.getopt(self.arg, 'hc:s:f:j', ['help', 'count=', 'select=', 'file=', 'json'])
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
                sys.exit()
            elif o in ("-c", "--count"):
                output = a
                print(f"""test - {output}""")
            elif o in ("-s", "--select"):
                select = a
                print(f"chel - {select}")
            elif o in ('-f', '--file'):
                self.file = a
                print(f"file - {self.file}")
            elif o in ('-j', '--json'):
                self.check_dir(self.HOME)
            else:
                assert False, 'unhandled option'


def hlp():
    count = sys.argv[1]
    for i in range(int(count)):
        try:
            ip=input("Введите ip:\n").split('.')
            ip.reverse()
            record = '.'.join(ip) + ".in-addr.arpa."
            check_pattern(ip)
            '''check_pattern = re.search(PATTERN, str('.'.join(ip)))
            if check_pattern:
                print(f"""############

                Check successfully {check_pattern.group()}

                ############""")
            else:
                print("Check not successfully")
                sys.exit(1)'''
            file = open(sys.argv[4], 'a')
            file.write(record.ljust(54) + f"{sys.argv[2]}   IN  PTR    " + sys.argv[3] + "." + '\n')
            file.close()
            tail(sys.argv[4], 4)
        except Exception as e:
            print(e)


def main():
    key_selection(sys.argv[1:])


if __name__ == '__main__':
    app = MyApp(sys.argv[1:])
    app.key_selection()
