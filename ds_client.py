# ds_client.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

import socket
import time

def create_socket(server:str, port:int) -> socket.socket:
    try:
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockt.connect((server, port))
        return sockt
    except:
        return None


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None) -> bool:
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    client = create_socket(server, port)
    if client == None:
        return False

    try:
        send = client.makefile('wb')
        msg = {"join": {"username": username, "password": password, "token": ""}}
        print(msg)
        #parse to json?
        send.write(msg + '\r\n')
        send.flush
        response = receive(server, port)
        print response
        return True
    except ValueError:
        return False

def receive(server:str, port:int):
    client = create_socket(server, port)
    if client == None:
        return None

    try: 
        recv = client.makefile('rb')
        srv_response = recv.readline()
        return srv_response
    except:
        Print('Error occured')


#TODO: return either True or False depending on results of required operation
