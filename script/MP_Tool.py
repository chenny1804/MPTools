# -*-coding:utf-8-*-
from socket import *
from time import sleep
import sys,os
HOST = '192.168.1.6'
PORT = 9034
BUFFSIZE = 1024
ADDR = (HOST, PORT)
RESULT_FILE_NAME="get_index_result.txt"
def read_command(filename):
    command_list=[]
    f=open(filename,"r")
    for line in f.readlines():
        command_list.append(line.split("\n")[0])
    return command_list
def write_result(filename,string):
    f=open(filename,"a")
    f.write(string)
    f.flush()
    f.close()
def main():
    try:
        UdpClientSocket = socket(AF_INET, SOCK_DGRAM)
        command_list=read_command("config.txt")
        if len(command_list)==0:
            print "no command"
            sys.exit(0)
        for command in command_list:
            UdpClientSocket.sendto(command, ADDR)
            data, addr = UdpClientSocket.recvfrom(BUFFSIZE)
            print "receiv data", data
            # sleep(1)
            if "/tmp/MP.txt ok" in data:
                UdpClientSocket.sendto("flash read", ADDR)
                data, addr = UdpClientSocket.recvfrom(BUFFSIZE)
                print "receiv <----", data
                # os.system("echo "+str(data) + " >> get_index.txt")
                write_result(RESULT_FILE_NAME,data)
    except Exception , e:
        print "Error:",e
        sys.exit(0)
if __name__ == '__main__':
    main()
