# -*-coding:utf-8-*-
import sys, getopt, os
from time import sleep
from Telnet import Telnet
from TranslateTheIndex import TranslateTheIndex, read_param_file

IP = "192.168.3.254"
USER_NAME = "admin"
PASSWORD = "admin"
PARAM_FILE_NAME = "param.txt"
TRANSLATE_PARAM = "Translate_param_"


def usage():
    print
    print "-----------------------------------------------------"
    print 'USAGE: write_and_check_index.py [OPTIONS]'
    print
    print ' OPTIONS:'
    print "\t -O user and password "
    print "\t -f the filename of set param"


def check_param(Tel):
 # check the param that telnet had set it
    read_param_list = read_param_file(PARAM_FILE_NAME)
    for line in read_param_list:
        param_list = line.split(":")[1].split("=")
        # print param_list
        param_key = param_list[0]
        param_value = param_list[1].split("\n")[0]
        # print "param_key",param_key,"param_value",param_value
        result = Tel.write_command("flash get " + param_key)
        for line1 in result.split("\r\n"):
            # print "line->", line1
            if param_key + "=" in line1:
                # print "line1",line1.split("=")
                # print "<<<line1" ,line1,"----",param_value
                if line1.split("=")[1]== param_value:
                     print "check ", param_key, " is OK"
                else:
                    print "check", param_key, "is Error"
            else:
                continue


def main():
    global PARAM_FILE_NAME
    global USER_NAME
    global PASSWORD
    global Tel
    try:
        if len(sys.argv) < 2:
            usage()
            sys.exit()
        opts, args = getopt.getopt(sys.argv[2:], "hO:f:", ["help", "password", "file"])
        IP = sys.argv[1]
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-O", "--password"):
                USER_NAME = a.split(":")[0]
                PASSWORD = a.split(":")[1]
                print "USER NAME:", USER_NAME
                print "PASSWORD:", PASSWORD
            if o in ("-f", "--filename"):
                print PARAM_FILE_NAME
                PARAM_FILE_NAME = a
        if os.path.exists("Trans_" + PARAM_FILE_NAME) == False:
            TranslateTheIndex(PARAM_FILE_NAME)
        Read_param_list = read_param_file("Trans_" + PARAM_FILE_NAME)
        print Read_param_list
        try:
            Tel = Telnet(USER_NAME, PASSWORD, IP, "23", "$", "Wireless AP login:", "Password:")
            Tel.login()
            for line in Read_param_list:
                print "Set Command:",line
                Tel.write_command(line.replace("\n",""))
            sleep(5)
            check_param(Tel)
            Tel.close()
        except Exception as e:
            print  IP, '\t\ttelnet not OK,May is not a ap', e
    except getopt.GetoptError, err:
        # print help information and exit:
        sys.stderr.write(str(err))
        usage()
        sys.exit()


if __name__ == '__main__':
    main()