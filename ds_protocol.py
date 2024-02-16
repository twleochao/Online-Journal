# ds_protocol.py

# Leo Chao
# ychao13@uci.edu 
# 76846188

import json
import socket
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

