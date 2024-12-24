#!/usr/bin/env python3
import sys
import getopt
import re
import os
import logging
import json

NAMEFILE: str = __file__.split("/")[-1].split(".")[0]
logging.basicConfig(level=logging.DEBUG, filename=f"/var/log/{NAMEFILE}.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
os.chown(f"/var/log/{NAMEFILE}.log", 501, 20)


class Base():

    HOME = os.path.expanduser("~")
    DIR_REVERS = os.path.join(HOME, ".revers")
    FILE_REVERS = os.path.join(HOME, ".revers/revers.json")
    DIR_ZONE = "/zones/"


    @staticmethod
    def send_error():
        return f"ERROR: check log: /var/log/{NAMEFILE}.log"


    @staticmethod
    def tail(fnam: str, k: int):
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
  -f, --file
  -c, --count
  -s, --select
  -j, --json                      check json file, if don't exist file then create this file

  Report bugs to <petryches.99@gmail.com>
        """)


    @staticmethod
    def check_pattern(text: str, pattern) -> None:
        search_pattern = re.search(pattern, text)
        if search_pattern:
            print(f"""############
            Check successfully {search_pattern.group()}
            ############""")
        else:
            print("Check not successfully")
            sys.exit(1)


    @staticmethod
    def my_check_json(self) -> bool:
        if os.path.isdir(self.DIR_REVERS) and os.path.isfile(self.FILE_REVERS):
            return True
        else:
            logging.error(f"{self.DIR_REVERS} or {self.FILE_REVERS} don't exists")
            return False


    @staticmethod
    def create_json_file(self):
        if os.path.isfile(self.FILE_REVERS):
            with open(os.path.join(self.DIR_REVERS, self.FILE_REVERS), "w") as filejs:
                filejs.write("""{
    "dir": ""
}
""")
        else:
            print("file don't exists")
            exit(os.EX_OSFILE)


    @staticmethod
    def check_dir(self, path = None) -> None:
        try:
            if self.my_check_json(self):
                logging.debug(f"\"{self.FILE_REVERS}\" exists")
            else:
                logging.debug(f"\"{self.FILE_REVERS}\" doesn't exists - Creating dir...")
                os.mkdir(self.DIR_REVERS)
                open(os.path.join(self.DIR_REVERS, self.FILE_REVERS), 'a').close()
                self.create_json_file(self)
                with open(os.path.join(self.DIR_REVERS, self.FILE_REVERS)) as filejs:
                    temp = json.load(filejs)
                    temp["dir"] = path
                with open(os.path.join(self.DIR_REVERS, self.FILE_REVERS), 'w') as filejs:
                    json.dump(temp, filejs, ensure_ascii=False, indent=4)
                logging.debug(f"\"{self.FILE_REVERS}\" created")
                print(f"please, fill out the file {self.FILE_REVERS}")
        except Exception as e:
            logging.error(e)
            print(self.send_error)
            sys.exit()


    @staticmethod
    def check_arg_for_json(self, arg):
        try:
            if self.my_check_json(self) == False:
                logging.debug(f"\"{self.FILE_REVERS}\" doesn't exists")
                raise f"\"{self.FILE_REVERS}\" doesn't exists"
            with open(self.FILE_REVERS) as j:
                jsn = json.load(j)
                j.close()
            json_list = list(jsn[arg][0].keys())
            return json_list
        except Exception as e:
            logging.error(e)
            print(self.send_error())
            sys.exit()


class MyApp(Base):

    PATTERN = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"

    def __init__(self,  arg):
        self.arg = arg
        file: str
        select: str
        file_for_json: str
        output: str


    def key_selection(self, *args):
        try:
            opts, args = getopt.getopt(self.arg, 'hc:s:f:j:', ['help', 'count=', 'select=', 'file=', 'json='])
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
                sys.exit()
            elif o in ("-c", "--count"):
                self.output = a
                print(self.check_arg_for_json(self, self.output))
                #self.check_arg_for_json(self, self.output)
                # print(f"""count - {self.output}""")
            elif o in ("-s", "--select"):
                print(f"select - {a}")
            elif o in ('-f', '--file'):
                self.file = a
                print(f"file - {self.file}")
            elif o in ('-j', '--json'):
                self.check_dir(self, str(a))q
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
