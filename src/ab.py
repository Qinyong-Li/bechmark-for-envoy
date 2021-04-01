import subprocess
import sys
import socket
import os


def help():
    print("pls input as fallow")
    print("python3 ab.py [$IP] [$PORT] [$PATH]")
    print("PATH: the path of url.txt")


def sendRequests(ip_port, urls_path):
    requests = [1, 10, 100, 1000]
    concurrency = [1, 10, 100, 1000]
    start_flag = "001"
    finished_flag = "010"
    close_flag = "011"
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(ip_port)

    for c in concurrency:
        for r in requests:
            filename = str(c)+"-"+str(r*c)+".data"
            soc.send(filename.encode("utf-8"))
            msg_rev = soc.recv(1024).decode("utf-8")
            if msg_rev != start_flag:
                return
            ab_filename = str(c)+"-"+str(c*r)+".txt"
            path = os.path.dirname(__file__)+"/../ "
            command = path+"ab -c " + \
                str(c)+" -n "+str(r*c)+" -L "+urls_path+">"+ab_filename
            prc = subprocess.Popen(command, shell=True)
            prc.wait()
            soc.send(finished_flag.encode("utf-8"))
    soc.send(close_flag.encode("utf-8"))


def main():
    argv = sys.argv
    length = len(argv)
    if length == 2 and argv[1] == "--help":
        help()
    elif length == 4:
        ip = argv[1]
        port = argv[2]
        urls_path = argv[3]
        ip_port = (ip, port)
        sendRequests(ip_port, urls_path)
    else:
        print("ab.py: wrong number of arguments")
        print()
        help()


print(os.path.dirname(__file__))
