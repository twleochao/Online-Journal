# a3.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

HOST = "168.235.86.101"
PORT = 3021

import socket
from ds_client import send 

def main():
    name = 'harharhahr'
    pwd = '123456789'
    msg = 'first post !!!'
    bio = 'this is my bio'
    send(HOST, PORT, name, pwd, msg, bio)

if __name__ == "__main__":
    main()
    


