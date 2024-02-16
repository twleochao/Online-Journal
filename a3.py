# a3.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

HOST = "168.235.86.101"
PORT = 3021

import socket
from ds_client import send 

def main():
    name = 'acbdfeuhf'
    pwd = '123456789'
    msg = 'testing FDHSJ FHDJSK '
    send(HOST, PORT, name, pwd, msg)

if __name__ == "__main__":
    main()
    


