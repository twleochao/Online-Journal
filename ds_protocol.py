# ds_protocol.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

import json
import socket
import time
from collections import namedtuple

class DSPServerError(Exception):
    pass

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys

ServerMessage = namedtuple('ServerMessage', ['type', 'message', 'token'])


def extract_json(json_msg:str) -> DSPConnection:
  '''
  Call the json.loads function on a json string and convert it to a DSPConnection object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
    try:
        json_obj = json.loads(json_msg)

        cmd = json_obj['response']['type']
        msg = ""
        tkn = ""
        if cmd == 'error':
            msg = json_obj['response']['message']
        elif cmd == 'ok':
            token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return ServerMessage(cmd, msg, tkn) 

def to_json(cmd: str, username:str, password:str, message:str, bio:str=None, token:str=None): 
    DSPcmd = None 
    if cmd == 'join':
        DSPcmd = {"join": {"username": username, "password": password, "token": ""}}
    elif cmd == 'bio':
        DSPcmd = {'token': token, 'bio': {'entry': bio, 'timestamp': time.time()}}
    elif cmd == 'post':
        DSPcmd = {'token': token, 'post': {'entry': message, 'timestamp': time.time()}}
    else:
        return DSPcmd



def get_send_msg(DSPcmd):
    msg = json.dumps(DSPcmd)
    return msg.encode()
