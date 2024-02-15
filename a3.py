# a3.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

HOST = "168.235.86.101"
PORT = 3021

import socket
from ds_client import create_socket 
from ds_protocol import init

main():
    sock = create_socket(HOST, PORT)
    connection = init(sock)


    

if __name__ == "__main__":
    main()
    


