#!/usr/bin/env python3
import sys
# import getopt
import re
import os
import logging
import json
from random import choices

from InquirerPy import inquirer

NAMEFILE: str = __file__.split("/")[-1].split(".")[0]
logging.basicConfig(level=logging.DEBUG, filename=f"/var/log/{NAMEFILE}.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
os.chown(f"/var/log/{NAMEFILE}.log", 501, 20)


class Base():

    HOME = os.path.expanduser("~")
    DIR_REVERS = os.path.join(HOME, ".revers")
    FILE_REVERS = os.path.join(HOME, ".revers/revers.json")
    DIR_ZONE = "/zones/"
    PATTERN = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"

    @staticmethod
    def send_error():
        return f"ERROR: check log: /var/log/{NAMEFILE}.log"


    @staticmethod
    def tail(fnam: str, k: int) -> None:
        try:
            with open(fnam,"r") as fi:
                txt=fi.readlines()
                count=len(txt)
                for i in range(count-k,count):
                    print(txt[i],end='')
        except Exception as a:
            print(a)


    @staticmethod
    def usage() -> None:
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
    def create_json_file(self) -> None:
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
    def check_dir(self, path: str = None) -> None:
        try:
            self.check_path(path)
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
                print(f"file {self.FILE_REVERS} exists")
        except Exception as e:
            logging.error(e)
            print(self.send_error)
            sys.exit()


    @staticmethod
    def check_arg_for_json(self, arg) -> None:# ВОЗМОЖНО НЕ НУЖЕН БУДЕТ
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


    @staticmethod
    def check_path(path: str) -> None:
        if os.path.isdir(path):
            print(f"{path} this directory exist")
            logging.debug(f"{path} this directory exist")
        else:
            print(f"{path} this directory does not exist")
            sys.exit(0)


    def show_path(self) -> str:
        with open(self.FILE_REVERS) as file:
            jsn = json.load(file)
        return jsn["dir"]


    # @staticmethod
    def list_dir(self) -> list:
        if os.path.isfile(self.FILE_REVERS):
            try:
                with open(self.FILE_REVERS) as file:
                    jsn = json.load(file)
                return [name for name in os.listdir(jsn["dir"]) if os.path.isdir(os.path.join(jsn["dir"], name))]
            except json.JSONDecodeError as e:
                logging.debug(e)


    @staticmethod
    def function():
        pass


    def write_down(self):
        path = self.show_path()
        zones: list = self.list_dir()
        ip = input("Введите ip: ").split('.')
        ip_str = '.'.join(ip)
        self.check_pattern(ip_str, self.PATTERN)
        ip.reverse()
        zone = inquirer.select(
            message="Выберите зону:",
            choices=zones,
        ).execute()
        domens: list = os.listdir(os.path.join(path, zone))
        domen = inquirer.select(
            message="Выберите домен: ",
            choices=domens,
        ).execute()
        full_path = os.path.join(path, zone, domen)
        file = open(full_path, "a")
        ip_str += ".in-addr.arpa."
        file.write()


    @staticmethod
    def hlp(self):
        count = sys.argv[1]
        for i in range(int(count)):
            try:
                ip = input("Введите ip:\n").split('.')
                self.check_pattern(ip, self.PATTERN)
                ip.reverse()
                record = '.'.join(ip) + ".in-addr.arpa."
                file = open(sys.argv[4], 'a')
                file.write(record.ljust(54) + f"{sys.argv[2]}   IN  PTR    " + sys.argv[3] + "." + '\n')
                file.close()
                self.tail(sys.argv[4], 4)
            except Exception as e:
                print(e)


class MyApp(Base):

    def __init__(self,  arg):
        self.arg = arg
        file: str
        output: str


    def key_selection(self, *args) -> None:
        import getopt
        try:
            opts, args = getopt.getopt(self.arg, 'hc:r:j:i:', ['help', 'count=', 'revers=', 'json=', 'ip='])
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                self.usage()
            elif o in ("-c", "--count"):
                self.output = a
                print(self.check_arg_for_json(self, self.output))# cкорее всего надо будет удалить
            elif o in ('-r', '--revers'):
                self.file = a
                print(f"file - {self.file}")
            elif o in ('-j', '--json'):
                self.check_dir(self, str(a))
            elif o in ('-i', '--ip'):
                self.write_down()
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


if __name__ == '__main__':
    app = MyApp(sys.argv[1:])
    app.key_selection()
