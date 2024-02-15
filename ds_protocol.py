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

DSPConnection = namedtuple('DSPConnection', ['socket','send', 'recv'])

def init(sock:socket) -> DSPConnection:
    try: 
        f_send = sock.makefile('wb')
        f_recv = sock.makefile('rb')
    except: 
        raise DSPServerError('Socket connection error')
    return DSPConnection(socket = sock, send = f_send, recv = f_recv)

def extract_json(json_msg:str) -> DSPConnection:
  '''
  Call the json.loads function on a json string and convert it to a DSPConnection object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)

    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)

def to_json(DSP_obj:DSPConnection) -> bytes
