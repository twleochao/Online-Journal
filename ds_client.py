# ds_client.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

import socket
from ds_protocol import to_json, get_send_msg, extract_json

def create_socket(server:str, port:int) -> socket.socket:
    try:
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockt.connect((server, port))
        return sockt
    except:
        return None

def receive(client:socket.socket):
    try: 
        recv = client.makefile('rb')
        srv_response = recv.readline()
        return srv_response
    except TypeError:
        print('Error occured')

def write_command(send, msg):
    send.write(msg + b'\r\n')
    send.flush()

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
    print(message)
    tkn = None
    client = create_socket(server, port)
    if client == None:
        return False

    try:
        send = client.makefile('wb')
        DSPcmd = to_json('join', username, password, message, bio)
        msg = get_send_msg(DSPcmd)
        write_command(send, msg)

        response = receive(client)
        serv_msg = extract_json(response)

        if serv_msg.type == 'error':
            print(serv_msg.message)
            return False
        tkn = serv_msg.token

        if bio != None:
            DSPcmd = to_json('bio', username, password, message, bio, tkn)
            msg = get_send_msg(DSPcmd)
            write_command(send, msg)
            response = receive(client)
            serv_msg = extract_json(response)
            print(serv_msg.message)
        if message != None:
            DSPcmd = to_json('post', username, password, message, bio, tkn)
            msg = get_send_msg(DSPcmd)
            write_command(send, msg)
            response = receive(client)
            serv_msg = extract_json(response)
            print(serv_msg.message)

        return True

    except ValueError:
        print('Missing information or invalid data type')
        return False
    #except:
        #print('Error occured')
        #return False
