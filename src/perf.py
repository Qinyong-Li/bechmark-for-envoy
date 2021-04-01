import sys
import subprocess
import socket


def help():
    print("python3 perf_record.py [$IP] [$PORT] [$PID] [$PADDWORD]")
    print("PID: pid of envoy")


def record_data(ip_port, port, password):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(ip_port)
    soc.listen(1)
    con, address = soc.accept()
    start_flag = "001"
    finished_flag = "010"
    close_flag = "011"
    while True:
        filename = con.recv().decode("utf-8")
        con.send(start_flag.encode("utf-8"))
        command = "sudo perf record -e cycles -p "+port
        proc = subprocess.Popen("echo %s|sudo -S %s"%(password, command),shell=True)
        msg_rev = con.recv().decode("utf=8")
        if msg_rev != finished_flag:
            exit()
        proc.terminate()
        if msg_rev == close_flag:
            break


